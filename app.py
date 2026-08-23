import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="PrediALL Facilidades",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Página inicial da aplicação."""

    st.markdown('<p class="main-header">🏢 PrediALL Facilidades</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Agente de Manutenção Predial com Inteligência Artificial</p>',
        unsafe_allow_html=True
    )

    st.divider()

    # Identificação do usuário (simplificada para MVP)
    if "usuario" not in st.session_state:
        st.session_state.usuario = None

    if st.session_state.usuario is None:
        st.subheader("👤 Identificação")
        st.info("Informe seus dados para acessar o sistema.")

        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome completo", placeholder="João da Silva")
            email = st.text_input("E-mail corporativo", placeholder="joao.silva@empresa.com")
        with col2:
            unidade = st.selectbox("Unidade", [
                "Selecione...",
                "Sede SP",
                "Filial RJ",
                "CD Guarulhos",
                "Cervejaria Boituva",
                "Cervejaria Petrópolis"
            ])
            ramal = st.text_input("Ramal (opcional)", placeholder="4532")

        perfil = st.radio(
            "Perfil de acesso",
            ["Solicitante", "Técnico", "Gestor"],
            horizontal=True
        )

        if st.button("🔓 Entrar", type="primary"):
            if nome and email and unidade != "Selecione...":
                st.session_state.usuario = {
                    "nome": nome,
                    "email": email,
                    "unidade": unidade,
                    "ramal": ramal,
                    "perfil": perfil
                }
                st.rerun()
            else:
                st.error("Preencha todos os campos obrigatórios.")
    else:
        # Usuário logado — mostrar menu principal
        usuario = st.session_state.usuario

        # Sidebar com info do usuário
        with st.sidebar:
            st.markdown(f"### 👤 {usuario['nome']}")
            st.caption(f"📧 {usuario['email']}")
            st.caption(f"🏢 {usuario['unidade']}")
            st.caption(f"🔑 Perfil: {usuario['perfil']}")
            st.divider()
            if st.button("🚪 Sair"):
                st.session_state.usuario = None
                st.rerun()

        # Cards de ação
        st.subheader(f"Olá, {usuario['nome'].split()[0]}! Como posso ajudar?")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 💬 Chat com Agente IA")
            st.write("Descreva seu problema em linguagem natural. O agente vai coletar os dados e abrir o chamado automaticamente.")
            if st.button("Iniciar Conversa", type="primary", key="btn_chat"):
                st.switch_page("pages/1_💬_Chat_Agente.py")

        with col2:
            st.markdown("### 📋 Formulário Rápido")
            st.write("Prefere preencher direto? Use o formulário estruturado para registrar seu chamado.")
            if st.button("Abrir Formulário", key="btn_form"):
                st.switch_page("pages/2_📋_Novo_Chamado.py")

        st.divider()

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("### 📊 Meus Chamados")
            st.write("Acompanhe o status dos seus chamados abertos e histórico de atendimentos.")
            if st.button("Ver Chamados", key="btn_chamados"):
                st.switch_page("pages/3_📊_Meus_Chamados.py")

        with col4:
            if usuario["perfil"] in ["Gestor", "Técnico"]:
                st.markdown("### 📈 Painel de Gestão")
                st.write("Dashboard com KPIs, chamados por categoria, SLA e satisfação.")
                if st.button("Abrir Painel", key="btn_painel"):
                    st.switch_page("pages/4_📈_Painel_Gestor.py")
            else:
                st.markdown("### ℹ️ Dicas")
                st.write(
                    "- Descreva o problema com detalhes\n"
                    "- Informe a localização exata\n"
                    "- Anexe fotos se possível\n"
                    "- Emergências: ligue ramal 9999"
                )


if __name__ == "__main__":
    main()
