"""
Serviço de banco de dados — Supabase (PostgreSQL).
Gerencia todas as operações CRUD de chamados.
"""

import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_client() -> Client:
    """Retorna cliente Supabase."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def criar_chamado(dados: dict) -> dict:
    """
    Cria um novo chamado no banco de dados.
    
    Args:
        dados: {
            unidade, local, tipo_ocorrencia, urgencia,
            descricao, solicitante_nome, solicitante_email,
            solicitante_ramal, categoria_ia, confianca_ia, criado_via
        }
    
    Returns:
        Registro criado com ID gerado.
    """
    client = get_client()

    registro = {
        "unidade": dados["unidade"],
        "local": dados["local"],
        "tipo_ocorrencia": dados["tipo_ocorrencia"],
        "urgencia": dados["urgencia"],
        "descricao": dados["descricao"],
        "solicitante_nome": dados["solicitante_nome"],
        "solicitante_email": dados["solicitante_email"],
        "solicitante_ramal": dados.get("solicitante_ramal", ""),
        "status": "Aberto",
        "categoria_ia": dados.get("categoria_ia", ""),
        "confianca_ia": dados.get("confianca_ia", 0),
        "criado_via": dados.get("criado_via", "Formulário"),
        "data_abertura": datetime.now().isoformat(),
    }

    response = client.table("chamados").insert(registro).execute()
    return response.data[0] if response.data else None


def listar_chamados_usuario(email: str) -> list:
    """Lista chamados de um solicitante específico."""
    client = get_client()
    response = (
        client.table("chamados")
        .select("*")
        .eq("solicitante_email", email)
        .order("data_abertura", desc=True)
        .execute()
    )
    return response.data


def listar_todos_chamados(filtros: dict = None) -> list:
    """Lista todos os chamados (para gestores). Aceita filtros opcionais."""
    client = get_client()
    query = client.table("chamados").select("*")

    if filtros:
        if filtros.get("unidade"):
            query = query.eq("unidade", filtros["unidade"])
        if filtros.get("status"):
            query = query.eq("status", filtros["status"])
        if filtros.get("urgencia"):
            query = query.eq("urgencia", filtros["urgencia"])
        if filtros.get("tipo_ocorrencia"):
            query = query.eq("tipo_ocorrencia", filtros["tipo_ocorrencia"])

    response = query.order("data_abertura", desc=True).execute()
    return response.data


def atualizar_status(chamado_id: int, novo_status: str, responsavel: str = None) -> dict:
    """Atualiza o status de um chamado."""
    client = get_client()
    dados = {"status": novo_status}

    if responsavel:
        dados["responsavel"] = responsavel
    if novo_status == "Concluído":
        dados["data_conclusao"] = datetime.now().isoformat()

    response = (
        client.table("chamados")
        .update(dados)
        .eq("id", chamado_id)
        .execute()
    )
    return response.data[0] if response.data else None


def registrar_avaliacao(chamado_id: int, nota: int, comentario: str = "") -> dict:
    """Registra a avaliação de satisfação do solicitante."""
    client = get_client()
    response = (
        client.table("chamados")
        .update({"nota_satisfacao": nota, "comentario_satisfacao": comentario})
        .eq("id", chamado_id)
        .execute()
    )
    return response.data[0] if response.data else None


def obter_estatisticas(unidade: str = None) -> dict:
    """Retorna estatísticas para o painel de gestão."""
    client = get_client()

    query = client.table("chamados").select("*")
    if unidade:
        query = query.eq("unidade", unidade)

    response = query.execute()
    chamados = response.data

    if not chamados:
        return {
            "total": 0, "abertos": 0, "em_andamento": 0,
            "concluidos": 0, "csat_medio": 0, "por_tipo": {},
            "por_urgencia": {}, "por_status": {}
        }

    abertos = [c for c in chamados if c["status"] == "Aberto"]
    em_andamento = [c for c in chamados if c["status"] == "Em Andamento"]
    concluidos = [c for c in chamados if c["status"] == "Concluído"]

    notas = [c["nota_satisfacao"] for c in chamados if c.get("nota_satisfacao")]
    csat_medio = sum(notas) / len(notas) if notas else 0

    # Contagem por tipo
    por_tipo = {}
    for c in chamados:
        tipo = c.get("tipo_ocorrencia", "Outros")
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1

    # Contagem por urgência
    por_urgencia = {}
    for c in chamados:
        urg = c.get("urgencia", "Normal")
        por_urgencia[urg] = por_urgencia.get(urg, 0) + 1

    # Contagem por status
    por_status = {}
    for c in chamados:
        status = c.get("status", "Aberto")
        por_status[status] = por_status.get(status, 0) + 1

    return {
        "total": len(chamados),
        "abertos": len(abertos),
        "em_andamento": len(em_andamento),
        "concluidos": len(concluidos),
        "csat_medio": round(csat_medio, 1),
        "por_tipo": por_tipo,
        "por_urgencia": por_urgencia,
        "por_status": por_status,
    }
