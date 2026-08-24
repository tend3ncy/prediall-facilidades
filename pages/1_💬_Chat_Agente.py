import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_agent import criar_agente, enviar_mensagem, extrair_dados_chamado, verificar_emergencia
from services.rag import buscar_contexto
from services.database import criar_chamado
from services.notifications import notificar_novo_chamado, notificar_emergencia

st.set_page_config(page_title="Chat - PrediALL", page_icon="💬", layout="wide")

st.title("💬 Chat com Agente de Facilities")

# Verificar se usuário está logado
if "usuario" not in st.session_state or st.session_state.usuario is None:
    st.warning("⚠️ Faça login na página inicial para acessar o chat.")
    if st.button("Ir para Login"):
        st.switch_page("app.py")
    st.stop()

usuario = st.session_state.usuario

# Inicializar estados
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chamado_criado" not in st.session_state:
    st.session_state.chamado_criado = False

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = None


def resetar_chat():
    st.session_state.messages = []
    st.session_state.chamado_criado = False
    st.session_state.system_prompt = None


# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {usuario['nome']}")
    st.caption(f"🏢 {usuario['unidade']}")
    st.divider()
    st.markdown("### 💡 Dicas")
    st.markdown(
        "- Descreva o problema naturalmente\n"
        "- O agente vai perguntar o que faltar\n"
        "- Diga a localização exata\n"
        "- Informe se é urgente"
    )
    st.divider()
    if st.button("🔄 Nova Conversa"):
        resetar_chat()
        st.rerun()

# Mensagem inicial
if not st.session_state.messages:
    saudacao = f"Olá, {usuario['nome'].split()[0]}! 👋 Sou o assistente de Facilities. Como posso ajudar você hoje? Descreva o problema que você está enfrentando."
    st.session_state.messages.append({"role": "assistant", "content": saudacao})

# Exibir todas as mensagens do histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Se chamado já foi criado
if st.session_state.chamado_criado:
    st.success("✅ Chamado registrado com sucesso! Clique em 'Nova Conversa' para abrir outro.")
    st.stop()

# Input do usuário
if prompt := st.chat_input("Descreva seu problema..."):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Processar resposta
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analisando..."):
            try:
                # Criar system prompt na primeira mensagem real do usuário
                if st.session_state.system_prompt is None:
                    contexto = buscar_contexto(prompt)
                    st.session_state.system_prompt = criar_agente(
                        nome_usuario=usuario["nome"],
                        unidade_usuario=usuario["unidade"],
                        contexto_rag=contexto,
                    )

                # Montar histórico para enviar ao modelo (sem a saudação inicial)
                historico_para_modelo = []
                for msg in st.session_state.messages[1:]:  # pula a saudação
                    if msg["role"] in ["user", "assistant"]:
                        historico_para_modelo.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })

                # Remover a última mensagem do user (será enviada separadamente)
                historico_enviar = historico_para_modelo[:-1]
                mensagem_atual = prompt

                # Enviar ao Groq com histórico completo
                resposta = enviar_mensagem(
                    st.session_state.system_prompt,
                    historico_enviar,
                    mensagem_atual
                )

                # Verificar emergência
                if verificar_emergencia(resposta):
                    resposta_limpa = resposta.split('{"emergencia"')[0].strip()
                    if not resposta_limpa:
                        resposta_limpa = "🚨 EMERGÊNCIA DETECTADA! Saia da área imediatamente. Brigada: ramal 9999, SAMU: 192, Bombeiros: 193."
                    st.markdown(resposta_limpa)
                    st.session_state.messages.append({"role": "assistant", "content": resposta_limpa})
                    notificar_emergencia({
                        "unidade": usuario["unidade"],
                        "local": "Informado no chat",
                        "tipo_ocorrencia": "EMERGÊNCIA",
                        "descricao": prompt,
                    })
                    st.error("🚨 Emergência notificada à equipe de segurança!")

                # Verificar se dados completos (chamado pronto)
                elif dados := extrair_dados_chamado(resposta):
                    resposta_limpa = resposta
                    if "```json" in resposta_limpa:
                        resposta_limpa = resposta_limpa.split("```json")[0].strip()
                    elif "```" in resposta_limpa:
                        resposta_limpa = resposta_limpa.split("```")[0].strip()
                    elif '{"completo"' in resposta_limpa:
                        resposta_limpa = resposta_limpa.split('{"completo"')[0].strip()

                    if not resposta_limpa:
                        resposta_limpa = "✅ Perfeito! Todos os dados foram coletados. Registrando seu chamado..."

                    st.markdown(resposta_limpa)
                    st.session_state.messages.append({"role": "assistant", "content": resposta_limpa})

                    # Criar chamado
                    chamado_dados = {
                        "unidade": usuario["unidade"],
                        "local": dados.get("local", ""),
                        "tipo_ocorrencia": dados.get("tipo_ocorrencia", dados.get("categoria_ia", "")),
                        "urgencia": dados.get("urgencia", "Normal"),
                        "descricao": dados.get("descricao", ""),
                        "solicitante_nome": usuario["nome"],
                        "solicitante_email": usuario["email"],
                        "solicitante_ramal": usuario.get("ramal", ""),
                        "categoria_ia": dados.get("categoria_ia", ""),
                        "confianca_ia": dados.get("confianca", 0),
                        "criado_via": "Chat IA",
                    }

                    resultado = criar_chamado(chamado_dados)
                    if resultado:
                        st.success(f"✅ **Chamado #{resultado['id']} criado com sucesso!**")
                        notificar_novo_chamado(resultado)
                        st.session_state.chamado_criado = True
                    else:
                        st.error("Erro ao criar chamado no banco. Tente novamente.")

                else:
                    # Resposta normal — agente ainda coletando dados
                    st.markdown(resposta)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})

            except Exception as e:
                erro_msg = f"Desculpe, tive um problema técnico. Tente novamente ou use o formulário. Erro: {str(e)}"
                st.error(erro_msg)
                st.session_state.messages.append({"role": "assistant", "content": erro_msg})
