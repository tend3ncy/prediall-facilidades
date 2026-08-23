"""
Serviço do Agente IA — Groq (LLaMA 3).
Gerencia o diálogo conversacional para coleta de dados de chamados.
"""

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "qwen/qwen3.6-27b"

SYSTEM_PROMPT = """/no_think
Você é o Assistente de Facilities da empresa. Sua função é ajudar 
colaboradores a registrar chamados de manutenção predial de forma rápida e completa.
IMPORTANTE: Responda APENAS com a mensagem final ao usuário. NÃO inclua blocos de raciocínio ou pensamento.

## Seu comportamento:
1. Cumprimente o usuário pelo nome (fornecido abaixo)
2. Pergunte como pode ajudar
3. Colete os seguintes dados OBRIGATÓRIOS (pergunte o que faltar):
   - Local exato (andar, sala, setor, área)
   - Tipo de problema (o que está acontecendo)
   - Urgência (qual o impacto: Crítica, Alta, Normal ou Baixa)
   - Descrição detalhada do problema
4. Classifique o problema em UMA das categorias:
   - Elétrica
   - Climatização / Refrigeração
   - Hidráulica
   - Limpeza / Higienização
   - Mobiliário
   - Infraestrutura
   - Predial Geral

5. Quando tiver TODOS os dados obrigatórios, confirme com o usuário um resumo e pergunte se está correto.

6. Se o usuário confirmar, responda com EXATAMENTE este formato JSON no final da mensagem (em um bloco separado):
```json
{"completo": true, "dados": {"local": "...", "tipo_ocorrencia": "...", "urgencia": "...", "descricao": "...", "categoria_ia": "...", "confianca": 95}}
```

## Regras INVIOLÁVEIS:

### Emergências (responda IMEDIATAMENTE):
Se detectar risco à vida (vazamento de gás/amônia, incêndio, risco elétrico grave, desabamento):
→ Responda: "🚨 **EMERGÊNCIA DETECTADA!** Saia da área imediatamente.
   - Brigada de Incêndio: ramal 9999
   - SAMU: 192
   - Bombeiros: 193
   NÃO tente resolver sozinho!"
→ Inclua: {"emergencia": true, "tipo_emergencia": "..."}

### Limites:
- NÃO forneça orientações técnicas de reparo
- NÃO autorize compras ou contratações
- Se não souber classificar com confiança > 80%, informe que vai direcionar para triagem humana
- Faça no MÁXIMO 2 perguntas por mensagem
- Seja objetivo e cordial

### Contexto de procedimentos (RAG):
{rag_context}
Se houver procedimento relevante, cite-o para orientar o solicitante (ex.: "Conforme PM-018, desligue o equipamento").
Se não houver contexto disponível, NÃO invente procedimentos.
"""


def criar_agente(nome_usuario: str, unidade_usuario: str, contexto_rag: str = "") -> str:
    """
    Cria o system prompt configurado para o agente.
    
    Returns:
        System prompt completo.
    """
    prompt_completo = SYSTEM_PROMPT.replace("{rag_context}", contexto_rag or "Nenhum contexto disponível.")
    prompt_completo += f"\n\n## Dados do solicitante:\n- Nome: {nome_usuario}\n- Unidade: {unidade_usuario}"
    return prompt_completo


def enviar_mensagem(system_prompt: str, historico: list, mensagem: str) -> str:
    """
    Envia uma mensagem ao agente e retorna a resposta.
    
    Args:
        system_prompt: Prompt do sistema configurado
        historico: Lista de mensagens anteriores [{"role": "user"/"assistant", "content": "..."}]
        mensagem: Nova mensagem do usuário
    
    Returns:
        Texto da resposta do agente.
    """
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(historico)
    messages.append({"role": "user", "content": mensagem})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=600,
        top_p=0.9,
    )

    resposta = response.choices[0].message.content

    # Remover bloco <think>...</think> que o Qwen3 pode incluir
    if "<think>" in resposta:
        resposta = re.sub(r"<think>[\s\S]*?</think>", "", resposta).strip()
    # Caso o </think> não feche, remover tudo antes dele
    if "</think>" in resposta:
        resposta = resposta.split("</think>")[-1].strip()
    # Caso só tenha <think> sem fechar, remover do <think> até o final ou até a resposta real
    if "<think>" in resposta:
        resposta = re.sub(r"<think>[\s\S]*", "", resposta).strip()

    return resposta


def extrair_dados_chamado(resposta: str) -> dict | None:
    """
    Tenta extrair o JSON de dados completos da resposta do agente.
    
    Returns:
        Dict com dados do chamado se completo, None caso contrário.
    """
    try:
        # Procura por JSON na resposta
        if '{"completo": true' in resposta or '{"completo":true' in resposta:
            # Extrai o JSON da resposta
            inicio = resposta.find('{"completo"')
            if inicio == -1:
                return None

            # Encontra o final do JSON contando chaves
            nivel = 0
            fim = inicio
            for i in range(inicio, len(resposta)):
                if resposta[i] == '{':
                    nivel += 1
                elif resposta[i] == '}':
                    nivel -= 1
                    if nivel == 0:
                        fim = i + 1
                        break

            json_str = resposta[inicio:fim]
            dados = json.loads(json_str)

            if dados.get("completo"):
                return dados.get("dados")

    except (json.JSONDecodeError, ValueError, IndexError):
        pass

    return None


def verificar_emergencia(resposta: str) -> bool:
    """Verifica se a resposta indica uma emergência."""
    return '"emergencia": true' in resposta or '"emergencia":true' in resposta
