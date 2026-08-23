"""
Serviço de RAG (Retrieval-Augmented Generation) — ChromaDB.
Indexa e busca procedimentos, normas e catálogo de ocorrências.
"""

import os
import chromadb
from chromadb.config import Settings


# Diretório persistente para o ChromaDB
CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_data")


def get_collection():
    """Retorna a collection do ChromaDB."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(
        name="knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )
    return collection


def indexar_documentos(documentos: list[dict]):
    """
    Indexa documentos na base vetorial.
    
    Args:
        documentos: Lista de {"id": str, "texto": str, "metadata": dict}
    """
    collection = get_collection()

    ids = [doc["id"] for doc in documentos]
    textos = [doc["texto"] for doc in documentos]
    metadatas = [doc.get("metadata", {}) for doc in documentos]

    collection.upsert(
        ids=ids,
        documents=textos,
        metadatas=metadatas,
    )

    return len(ids)


def buscar_contexto(query: str, n_resultados: int = 3) -> str:
    """
    Busca os trechos mais relevantes da base de conhecimento.
    
    Args:
        query: Texto da consulta (descrição do problema)
        n_resultados: Número de resultados a retornar
    
    Returns:
        Texto concatenado dos trechos relevantes para usar como contexto.
    """
    collection = get_collection()

    # Verifica se há documentos indexados
    if collection.count() == 0:
        return ""

    results = collection.query(
        query_texts=[query],
        n_results=min(n_resultados, collection.count()),
    )

    if not results["documents"] or not results["documents"][0]:
        return ""

    # Monta o contexto com os trechos recuperados
    contexto_partes = []
    for i, (doc, metadata) in enumerate(
        zip(results["documents"][0], results["metadatas"][0])
    ):
        fonte = metadata.get("fonte", "Documento interno")
        categoria = metadata.get("categoria", "")
        contexto_partes.append(
            f"[Fonte: {fonte} | Categoria: {categoria}]\n{doc}"
        )

    return "\n\n---\n\n".join(contexto_partes)


def carregar_base_conhecimento():
    """
    Carrega os documentos padrão da base de conhecimento.
    Chamado pelo setup_knowledge_base.py.
    """
    documentos = [
        # Procedimentos de Climatização
        {
            "id": "pm-018",
            "texto": (
                "Procedimento PM-018: Vazamento em Aparelho Split. "
                "Categoria: Climatização > Vazamento. SLA: 4 horas. "
                "Orientação ao solicitante: 1) Desligue o aparelho pelo controle ou disjuntor. "
                "2) Coloque um recipiente embaixo do vazamento. "
                "3) Afaste equipamentos eletrônicos da área molhada. "
                "4) Não tente abrir o equipamento. 5) Aguarde o técnico. "
                "EPI obrigatório para o técnico: Luvas, óculos de proteção."
            ),
            "metadata": {"fonte": "PM-018", "categoria": "Climatização"},
        },
        {
            "id": "pm-019-amonia",
            "texto": (
                "EMERGÊNCIA - Vazamento de Amônia (Refrigeração Industrial). "
                "AÇÃO IMEDIATA: EVACUE A ÁREA. Ligue Brigada: ramal 9999, SAMU: 192, Bombeiros: 193. "
                "NÃO retorne ao local até liberação da SST. "
                "Sinais: odor forte e irritante, irritação nos olhos/nariz/garganta, "
                "névoa branca próxima a equipamentos de refrigeração."
            ),
            "metadata": {"fonte": "PM-019", "categoria": "Emergência"},
        },
        # Procedimentos Elétricos
        {
            "id": "pm-005",
            "texto": (
                "Procedimento PM-005: Queda de Energia Parcial. "
                "Categoria: Elétrica > Queda parcial. SLA: 2 horas. "
                "Orientação ao solicitante: 1) NÃO toque no quadro elétrico. "
                "2) Desligue equipamentos sensíveis pelos estabilizadores. "
                "3) Anote quais equipamentos/tomadas estão sem energia. "
                "4) Sinalize se algo ligado deveria estar desligado. "
                "5) Aguarde o eletricista. "
                "Conforme NR-10: somente profissionais autorizados podem intervir."
            ),
            "metadata": {"fonte": "PM-005", "categoria": "Elétrica"},
        },
        {
            "id": "nr-10-resumo",
            "texto": (
                "Norma NR-10: Segurança em Instalações Elétricas. "
                "Princípios: Somente profissionais autorizados podem intervir em instalações elétricas. "
                "O solicitante NUNCA deve tentar fazer reparos elétricos. "
                "Equipamentos com faísca ou cheiro de queimado: desligar disjuntor e evacuar. "
                "Trabalho em painéis: desligar, bloquear, sinalizar, testar ausência de tensão."
            ),
            "metadata": {"fonte": "NR-10", "categoria": "Norma de Segurança"},
        },
        # Procedimentos Hidráulicos
        {
            "id": "pm-031",
            "texto": (
                "Procedimento PM-031: Entupimento de Rede Hidráulica. "
                "Categoria: Hidráulica > Entupimento. SLA: 4 horas. "
                "Orientação ao solicitante: 1) Não use o equipamento entupido. "
                "2) Se houver transbordamento, feche o registro mais próximo. "
                "3) Sinalize o local com 'Interditado'. "
                "4) Não jogue produtos químicos (pode danificar a tubulação)."
            ),
            "metadata": {"fonte": "PM-031", "categoria": "Hidráulica"},
        },
        {
            "id": "pm-032-vazamento",
            "texto": (
                "Procedimento PM-032: Vazamento de Água. "
                "Categoria: Hidráulica > Vazamento. "
                "Vazamento pequeno: SLA 8h. Colocar recipiente, fechar registro se acessível. "
                "Vazamento grande/inundação: SLA 1h. Fechar registro geral do andar. "
                "Chamar coordenador imediatamente se inundação."
            ),
            "metadata": {"fonte": "PM-032", "categoria": "Hidráulica"},
        },
        # NR-35
        {
            "id": "nr-35-resumo",
            "texto": (
                "Norma NR-35: Trabalho em Altura. "
                "Qualquer atividade acima de 2 metros = Trabalho em Altura. "
                "Requer: PT (Permissão de Trabalho), ASO específico, equipamentos certificados. "
                "Chamados que envolvem altura (luminária em galpão, reparo em telhado) "
                "devem ter SLA ajustado para incluir tempo de preparação da PT. "
                "Aplicável a: telhado, fachada, mezanino, galpão alto."
            ),
            "metadata": {"fonte": "NR-35", "categoria": "Norma de Segurança"},
        },
        # Catálogo geral
        {
            "id": "cat-limpeza",
            "texto": (
                "Catálogo: Limpeza e Higienização. "
                "Limpeza emergencial (derramamento): SLA 30min. Sinalizar área molhada. "
                "Banheiro sem material: SLA 1h. "
                "Lixeiras cheias: SLA 2h. "
                "Odor forte: SLA 4h. Ventilar o ambiente se possível. "
                "Limpeza de rotina não realizada: SLA 8h."
            ),
            "metadata": {"fonte": "Catálogo", "categoria": "Limpeza"},
        },
        {
            "id": "cat-mobiliario",
            "texto": (
                "Catálogo: Mobiliário. "
                "Cadeira quebrada: SLA 48h. Não usar, sinalizar. "
                "Mesa/bancada danificada: SLA 48h. "
                "Porta/janela com defeito: SLA 24h. Não forçar. "
                "Fechadura/tranca com problema: SLA 8h. Não trancar a porta. "
                "Divisória danificada: SLA 72h."
            ),
            "metadata": {"fonte": "Catálogo", "categoria": "Mobiliário"},
        },
        {
            "id": "cat-infraestrutura",
            "texto": (
                "Catálogo: Infraestrutura e Docas. "
                "Portão de doca com defeito: SLA 2h. Operar manualmente se seguro. "
                "Piso danificado/buraco: SLA 4h. Sinalizar com cone. "
                "Rachadura em parede/pilar: SLA 24h. Evacuar se parecer estrutural. "
                "Elevador parado: SLA 1h. Se alguém preso: acionar bombeiros. "
                "Nivelador de doca quebrado: SLA 2h. Não usar a doca."
            ),
            "metadata": {"fonte": "Catálogo", "categoria": "Infraestrutura"},
        },
        # Regras de escalonamento
        {
            "id": "regras-escalonamento",
            "texto": (
                "Regras de Escalonamento Automático: "
                "Urgência Crítica + tipo Elétrica/Hidráulica/Climatização: "
                "notificar Coordenador + Técnico imediatamente. "
                "Chamado não atendido em 50% do SLA: alerta amarelo para coordenador. "
                "Chamado não atendido em 100% do SLA: alerta vermelho para gestor. "
                "3+ chamados iguais no mesmo local em 30 dias: flag problema recorrente."
            ),
            "metadata": {"fonte": "Regras Internas", "categoria": "Escalonamento"},
        },
    ]

    total = indexar_documentos(documentos)
    return total
