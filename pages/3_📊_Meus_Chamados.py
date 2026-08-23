import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database import listar_chamados_usuario, registrar_avaliacao

st.set_page_config(page_title="Meus Chamados - PrediALL", page_icon="📊", layout="wide")

st.title("📊 Meus Chamados")

# Verificar login
if "usuario" not in st.session_state or st.session_state.usuario is None:
    st.warning("⚠️ Faça login na página inicial para acessar.")
    if st.button("Ir para Login"):
        st.switch_page("app.py")
    st.stop()

usuario = st.session_state.usuario

st.info(f"👤 **{usuario['nome']}** | 🏢 {usuario['unidade']}")

# Filtros
col_filtro1, col_filtro2 = st.columns(2)
with col_filtro1:
    filtro_status = st.multiselect(
        "Filtrar por Status",
        ["Aberto", "Em Triagem", "Em Andamento", "Pendente", "Concluído", "Cancelado"],
        default=["Aberto", "Em Triagem", "Em Andamento", "Pendente"]
    )
with col_filtro2:
    filtro_urgencia = st.multiselect(
        "Filtrar por Urgência",
        ["Crítica", "Alta", "Normal", "Baixa"],
        default=[]
    )

st.divider()

# Buscar chamados
chamados = listar_chamados_usuario(usuario["email"])

if not chamados:
    st.info("📭 Você ainda não tem chamados registrados. Use o Chat ou o Formulário para abrir seu primeiro chamado!")
    st.stop()

# Aplicar filtros
if filtro_status:
    chamados = [c for c in chamados if c.get("status") in filtro_status]
if filtro_urgencia:
    chamados = [c for c in chamados if c.get("urgencia") in filtro_urgencia]

# Métricas resumo
total = len(chamados)
abertos = len([c for c in chamados if c["status"] in ["Aberto", "Em Triagem", "Em Andamento"]])
concluidos = len([c for c in chamados if c["status"] == "Concluído"])

col1, col2, col3 = st.columns(3)
col1.metric("Total", total)
col2.metric("Em Aberto", abertos)
col3.metric("Concluídos", concluidos)

st.divider()

# Lista de chamados
for chamado in chamados:
    # Cores por status
    status_colors = {
        "Aberto": "🟠",
        "Em Triagem": "🔵",
        "Em Andamento": "🔵",
        "Pendente": "🔴",
        "Concluído": "🟢",
        "Cancelado": "⚫",
    }

    urgencia_colors = {
        "Crítica": "🚨",
        "Alta": "🔴",
        "Normal": "🟡",
        "Baixa": "🟢",
    }

    status_emoji = status_colors.get(chamado.get("status", ""), "⚪")
    urgencia_emoji = urgencia_colors.get(chamado.get("urgencia", ""), "⚪")

    with st.expander(
        f"{status_emoji} **#{chamado['id']}** — {chamado.get('tipo_ocorrencia', 'N/A')} | "
        f"{chamado.get('local', '')} | {urgencia_emoji} {chamado.get('urgencia', '')}"
    ):
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"**Status:** {status_emoji} {chamado.get('status', 'N/A')}")
            st.markdown(f"**Tipo:** {chamado.get('tipo_ocorrencia', 'N/A')}")
            st.markdown(f"**Urgência:** {urgencia_emoji} {chamado.get('urgencia', 'N/A')}")
            st.markdown(f"**Local:** {chamado.get('unidade', '')} — {chamado.get('local', '')}")

        with col_b:
            st.markdown(f"**Aberto em:** {chamado.get('data_abertura', 'N/A')[:16]}")
            if chamado.get("data_conclusao"):
                st.markdown(f"**Concluído em:** {chamado['data_conclusao'][:16]}")
            if chamado.get("responsavel"):
                st.markdown(f"**Responsável:** {chamado['responsavel']}")
            st.markdown(f"**Via:** {chamado.get('criado_via', 'N/A')}")

        st.markdown(f"**Descrição:** {chamado.get('descricao', 'N/A')}")

        # Avaliação de satisfação (se concluído e não avaliado)
        if chamado.get("status") == "Concluído" and not chamado.get("nota_satisfacao"):
            st.divider()
            st.markdown("### ⭐ Avalie o atendimento")
            nota = st.slider(
                "Nota",
                1, 5, 4,
                key=f"nota_{chamado['id']}",
                help="1 = Péssimo, 5 = Excelente"
            )
            comentario = st.text_input(
                "Comentário (opcional)",
                key=f"comentario_{chamado['id']}"
            )
            if st.button("Enviar Avaliação", key=f"btn_avaliar_{chamado['id']}"):
                registrar_avaliacao(chamado["id"], nota, comentario)
                st.success("✅ Avaliação registrada! Obrigado pelo feedback.")
                st.rerun()
        elif chamado.get("nota_satisfacao"):
            st.markdown(f"⭐ **Avaliação:** {'⭐' * chamado['nota_satisfacao']} ({chamado['nota_satisfacao']}/5)")
