"""
Script para popular o banco com dados de demonstração.
Execute uma vez para ter chamados de exemplo no sistema.
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Dados de demonstração
chamados_demo = [
    {
        "unidade": "Sede SP",
        "local": "4º andar, sala 405",
        "tipo_ocorrencia": "Climatização / Refrigeração",
        "urgencia": "Alta",
        "descricao": "Ar-condicionado split vazando água no chão, próximo a equipamentos eletrônicos. Já colocamos balde mas está piorando.",
        "solicitante_nome": "Maria Santos",
        "solicitante_email": "maria.santos@empresa.com",
        "solicitante_ramal": "4532",
        "status": "Em Andamento",
        "responsavel": "Carlos Técnico HVAC",
        "categoria_ia": "Climatização / Refrigeração",
        "confianca_ia": 97,
        "criado_via": "Chat IA",
        "data_abertura": (datetime.now() - timedelta(hours=3)).isoformat(),
        "nota_satisfacao": None,
    },
    {
        "unidade": "Sede SP",
        "local": "2º andar, copa principal",
        "tipo_ocorrencia": "Hidráulica",
        "urgencia": "Normal",
        "descricao": "Torneira da copa pingando mesmo quando fechada completamente. Desperdício de água.",
        "solicitante_nome": "João Silva",
        "solicitante_email": "joao.silva@empresa.com",
        "solicitante_ramal": "4210",
        "status": "Aberto",
        "responsavel": None,
        "categoria_ia": "Hidráulica",
        "confianca_ia": 94,
        "criado_via": "Formulário",
        "data_abertura": (datetime.now() - timedelta(hours=1)).isoformat(),
        "nota_satisfacao": None,
    },
    {
        "unidade": "CD Guarulhos",
        "local": "Doca 03 - Área de carga",
        "tipo_ocorrencia": "Infraestrutura (Docas, Estrutural)",
        "urgencia": "Crítica",
        "descricao": "Portão da doca 03 travou na posição aberta, não fecha de jeito nenhum. Impossível receber caminhões nessa doca.",
        "solicitante_nome": "Pedro Oliveira",
        "solicitante_email": "pedro.oliveira@empresa.com",
        "solicitante_ramal": "3101",
        "status": "Em Andamento",
        "responsavel": "Marcos Manutenção Industrial",
        "categoria_ia": "Infraestrutura",
        "confianca_ia": 99,
        "criado_via": "Chat IA",
        "data_abertura": (datetime.now() - timedelta(hours=5)).isoformat(),
        "nota_satisfacao": None,
    },
    {
        "unidade": "Filial RJ",
        "local": "1º andar, recepção",
        "tipo_ocorrencia": "Elétrica",
        "urgencia": "Normal",
        "descricao": "Duas luminárias da recepção estão apagadas há 3 dias. Ambiente está escuro para visitantes.",
        "solicitante_nome": "Ana Costa",
        "solicitante_email": "ana.costa@empresa.com",
        "solicitante_ramal": "5001",
        "status": "Concluído",
        "responsavel": "Roberto Eletricista",
        "categoria_ia": "Elétrica",
        "confianca_ia": 92,
        "criado_via": "Formulário",
        "data_abertura": (datetime.now() - timedelta(days=2)).isoformat(),
        "data_conclusao": (datetime.now() - timedelta(days=1)).isoformat(),
        "nota_satisfacao": 5,
        "comentario_satisfacao": "Rápido e eficiente!",
    },
    {
        "unidade": "Cervejaria Boituva",
        "local": "Linha 02 - Envasamento, painel elétrico P-04",
        "tipo_ocorrencia": "Elétrica",
        "urgencia": "Crítica",
        "descricao": "Tomada próxima à esteira de envasamento soltando faísca ao ligar equipamento. Risco de curto-circuito. Desligamos o disjuntor.",
        "solicitante_nome": "Carlos Mendes",
        "solicitante_email": "carlos.mendes@empresa.com",
        "solicitante_ramal": "7042",
        "status": "Em Andamento",
        "responsavel": "Fábio Eletricista NR-10",
        "categoria_ia": "Elétrica",
        "confianca_ia": 98,
        "criado_via": "Chat IA",
        "data_abertura": (datetime.now() - timedelta(hours=2)).isoformat(),
        "nota_satisfacao": None,
    },
    {
        "unidade": "Sede SP",
        "local": "3º andar, banheiro masculino",
        "tipo_ocorrencia": "Hidráulica",
        "urgencia": "Alta",
        "descricao": "Vaso sanitário entupido e transbordando. Banheiro interditado. Urgente.",
        "solicitante_nome": "Ricardo Ferreira",
        "solicitante_email": "ricardo.ferreira@empresa.com",
        "solicitante_ramal": "4315",
        "status": "Concluído",
        "responsavel": "José Encanador",
        "categoria_ia": "Hidráulica",
        "confianca_ia": 96,
        "criado_via": "Chat IA",
        "data_abertura": (datetime.now() - timedelta(days=1, hours=4)).isoformat(),
        "data_conclusao": (datetime.now() - timedelta(days=1, hours=1)).isoformat(),
        "nota_satisfacao": 4,
        "comentario_satisfacao": "Resolvido, mas demorou um pouco.",
    },
    {
        "unidade": "CD Guarulhos",
        "local": "Escritório administrativo, sala 02",
        "tipo_ocorrencia": "Mobiliário",
        "urgencia": "Baixa",
        "descricao": "Cadeira do escritório com encosto quebrado. Não oferece suporte lombar.",
        "solicitante_nome": "Fernanda Lima",
        "solicitante_email": "fernanda.lima@empresa.com",
        "solicitante_ramal": "3205",
        "status": "Aberto",
        "responsavel": None,
        "categoria_ia": "Mobiliário",
        "confianca_ia": 91,
        "criado_via": "Formulário",
        "data_abertura": (datetime.now() - timedelta(hours=6)).isoformat(),
        "nota_satisfacao": None,
    },
    {
        "unidade": "Cervejaria Petrópolis",
        "local": "Galpão de armazenamento, corredor B",
        "tipo_ocorrencia": "Limpeza / Higienização",
        "urgencia": "Normal",
        "descricao": "Derramamento de líquido no corredor B do galpão. Piso escorregadio. Já sinalizamos com cone.",
        "solicitante_nome": "Thiago Souza",
        "solicitante_email": "thiago.souza@empresa.com",
        "solicitante_ramal": "8100",
        "status": "Concluído",
        "responsavel": "Equipe Limpeza",
        "categoria_ia": "Limpeza / Higienização",
        "confianca_ia": 95,
        "criado_via": "Chat IA",
        "data_abertura": (datetime.now() - timedelta(days=3)).isoformat(),
        "data_conclusao": (datetime.now() - timedelta(days=3, hours=-1)).isoformat(),
        "nota_satisfacao": 5,
        "comentario_satisfacao": "Limparam em menos de 30 minutos!",
    },
    {
        "unidade": "Sede SP",
        "local": "Térreo, estacionamento subsolo 1",
        "tipo_ocorrencia": "Elétrica",
        "urgencia": "Normal",
        "descricao": "Sensor de iluminação automática do subsolo 1 não está funcionando. Luzes ficam acesas 24h.",
        "solicitante_nome": "Luciana Martins",
        "solicitante_email": "luciana.martins@empresa.com",
        "solicitante_ramal": "4001",
        "status": "Pendente",
        "responsavel": "Roberto Eletricista",
        "categoria_ia": "Elétrica",
        "confianca_ia": 88,
        "criado_via": "Formulário",
        "data_abertura": (datetime.now() - timedelta(days=4)).isoformat(),
        "nota_satisfacao": None,
    },
    {
        "unidade": "Filial RJ",
        "local": "5º andar, sala de reunião 3",
        "tipo_ocorrencia": "Climatização / Refrigeração",
        "urgencia": "Normal",
        "descricao": "Ar-condicionado da sala de reunião 3 fazendo barulho excessivo. Impossível fazer reuniões com áudio.",
        "solicitante_nome": "Bruno Almeida",
        "solicitante_email": "bruno.almeida@empresa.com",
        "solicitante_ramal": "5312",
        "status": "Aberto",
        "responsavel": None,
        "categoria_ia": "Climatização / Refrigeração",
        "confianca_ia": 93,
        "criado_via": "Chat IA",
        "data_abertura": (datetime.now() - timedelta(hours=8)).isoformat(),
        "nota_satisfacao": None,
    },
]


def main():
    print("=" * 60)
    print("  PrediALL Facilidades — Inserindo dados de demonstração")
    print("=" * 60)
    print()

    # Limpar dados existentes (opcional)
    print("Limpando dados antigos...")
    client.table("chamados").delete().neq("id", 0).execute()
    print("✅ Tabela limpa.")
    print()

    # Inserir dados de demo
    print(f"Inserindo {len(chamados_demo)} chamados de demonstração...")
    for i, chamado in enumerate(chamados_demo, 1):
        # Remover campos None para não enviar ao Supabase
        dados_limpos = {k: v for k, v in chamado.items() if v is not None}
        client.table("chamados").insert(dados_limpos).execute()
        print(f"  [{i}/{len(chamados_demo)}] {chamado['tipo_ocorrencia']} — {chamado['unidade']} ({chamado['status']})")

    print()
    print("=" * 60)
    print("✅ 10 chamados de demonstração inseridos com sucesso!")
    print()
    print("Resumo:")
    print("  • 3 Abertos")
    print("  • 3 Em Andamento")
    print("  • 3 Concluídos")
    print("  • 1 Pendente")
    print()
    print("  • 2 Críticos, 2 Altos, 5 Normais, 1 Baixo")
    print("  • 5 unidades diferentes")
    print("  • 3 avaliações de satisfação (média 4.7/5)")
    print("=" * 60)


if __name__ == "__main__":
    main()
