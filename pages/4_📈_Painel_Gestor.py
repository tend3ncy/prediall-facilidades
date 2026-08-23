import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database import obter_estatisticas, listar_todos_chamados, atualizar_status

st.set_page_config(page_title="Painel Gestor - PrediALL", page_icon="📈", layout="wide")

st.title("📈 Painel de Gestão — Facilities")

# Verificar login e perfil
if "usuario" not in st.session_state or st.session_state.usuario is None:
    st.warning("⚠️ Faça login na página inicial para acessar.")
    if st.button("Ir para Login"):
        st.switch_page("app.py")
    st.stop()

usuario = st.session_state.usuario

if usuario["perfil"] not in ["Gestor", "Técnico"]:
    st.error("🔒 Acesso restrito. Apenas Gestores e Técnicos podem acessar este painel.")
    st.stop()

# Filtro de unidade
with st.sidebar:
    st.markdown(f"### 👤 {usuario['nome']}")
    st.caption(f"🔑 {usuario['perfil']}")
    st.divider()
    filtro_unidade = st.selectbox(
        "🏢 Filtrar por Unidade",
        ["Todas", "Sede SP", "Filial RJ", "CD Guarulhos", "Cervejaria Boituva", "Cervejaria Petrópolis"]
    )

unidade_filtro = None if filtro_unidade == "Todas" else filtro_unidade

# Obter estatísticas
stats = obter_estatisticas(unidade_filtro)

# KPIs principais
st.subheader("📊 Indicadores Principais")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📋 Total", stats["total"])
col2.metric("🟠 Abertos", stats["abertos"])
col3.metric("🔵 Em Andamento", stats["em_andamento"])
col4.metric("🟢 Concluídos", stats["concluidos"])
col5.metric("⭐ CSAT Médio", f"{stats['csat_medio']}/5.0")

st.divider()

# Gráficos
if stats["total"] > 0:
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("🔧 Chamados por Tipo")
        if stats["por_tipo"]:
            df_tipo = pd.DataFrame(
                list(stats["por_tipo"].items()),
                columns=["Tipo", "Quantidade"]
            )
            fig_tipo = px.bar(
                df_tipo,
                x="Tipo",
                y="Quantidade",
                color="Tipo",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_tipo.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig_tipo, use_container_width=True)

    with col_graf2:
        st.subheader("⚡ Distribuição por Urgência")
        if stats["por_urgencia"]:
            df_urg = pd.DataFrame(
                list(stats["por_urgencia"].items()),
                columns=["Urgência", "Quantidade"]
            )
            cores_urgencia = {
                "Crítica": "#FF4444",
                "Alta": "#FF8C00",
                "Normal": "#FFD700",
                "Baixa": "#32CD32"
            }
            df_urg["Cor"] = df_urg["Urgência"].map(cores_urgencia)

            fig_urg = px.pie(
                df_urg,
                values="Quantidade",
                names="Urgência",
                color="Urgência",
                color_discrete_map=cores_urgencia
            )
            fig_urg.update_layout(height=350)
            st.plotly_chart(fig_urg, use_container_width=True)

    # Status geral
    st.subheader("📈 Status dos Chamados")
    if stats["por_status"]:
        df_status = pd.DataFrame(
            list(stats["por_status"].items()),
            columns=["Status", "Quantidade"]
        )
        fig_status = px.bar(
            df_status,
            x="Status",
            y="Quantidade",
            color="Status",
            color_discrete_map={
                "Aberto": "#FFA500",
                "Em Triagem": "#4169E1",
                "Em Andamento": "#1E90FF",
                "Pendente": "#DC143C",
                "Concluído": "#32CD32",
                "Cancelado": "#808080"
            }
        )
        fig_status.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig_status, use_container_width=True)

    st.divider()

    # Tabela de chamados (para gestão)
    st.subheader("📋 Lista de Chamados")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filtro_status_tabela = st.selectbox(
            "Status", ["Todos", "Aberto", "Em Andamento", "Pendente", "Concluído"]
        )
    with col_f2:
        filtro_urgencia_tabela = st.selectbox(
            "Urgência", ["Todas", "Crítica", "Alta", "Normal", "Baixa"]
        )
    with col_f3:
        filtro_tipo_tabela = st.selectbox(
            "Tipo", ["Todos", "Elétrica", "Climatização / Refrigeração", "Hidráulica",
                     "Limpeza / Higienização", "Mobiliário", "Infraestrutura", "Predial Geral"]
        )

    filtros = {}
    if unidade_filtro:
        filtros["unidade"] = unidade_filtro
    if filtro_status_tabela != "Todos":
        filtros["status"] = filtro_status_tabela
    if filtro_urgencia_tabela != "Todas":
        filtros["urgencia"] = filtro_urgencia_tabela
    if filtro_tipo_tabela != "Todos":
        filtros["tipo_ocorrencia"] = filtro_tipo_tabela

    chamados = listar_todos_chamados(filtros if filtros else None)

    if chamados:
        df = pd.DataFrame(chamados)
        colunas_exibir = [
            "id", "unidade", "local", "tipo_ocorrencia",
            "urgencia", "status", "solicitante_nome", "data_abertura"
        ]
        colunas_existentes = [c for c in colunas_exibir if c in df.columns]
        st.dataframe(
            df[colunas_existentes],
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", width="small"),
                "unidade": "Unidade",
                "local": "Local",
                "tipo_ocorrencia": "Tipo",
                "urgencia": "Urgência",
                "status": "Status",
                "solicitante_nome": "Solicitante",
                "data_abertura": st.column_config.DatetimeColumn("Abertura", format="DD/MM/YYYY HH:mm"),
            }
        )

        # Ação rápida: atualizar status
        st.divider()
        st.subheader("⚡ Ação Rápida")
        col_acao1, col_acao2, col_acao3 = st.columns(3)
        with col_acao1:
            chamado_id = st.number_input("ID do Chamado", min_value=1, step=1)
        with col_acao2:
            novo_status = st.selectbox(
                "Novo Status",
                ["Em Triagem", "Em Andamento", "Pendente", "Concluído", "Cancelado"]
            )
        with col_acao3:
            responsavel = st.text_input("Responsável (opcional)")

        if st.button("Atualizar Status", type="primary"):
            resultado = atualizar_status(chamado_id, novo_status, responsavel or None)
            if resultado:
                st.success(f"✅ Chamado #{chamado_id} atualizado para '{novo_status}'")
                st.rerun()
            else:
                st.error("❌ Erro ao atualizar. Verifique o ID do chamado.")
    else:
        st.info("Nenhum chamado encontrado com os filtros selecionados.")

else:
    st.info("📭 Nenhum chamado registrado ainda. Os dados aparecerão aqui conforme os chamados forem criados.")
