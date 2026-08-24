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

# CSS customizado para visual moderno
st.markdown("""
<style>
    /* Reset e base */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header principal */
    .hero-section {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0ea5e9 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(14, 165, 233, 0.15);
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 0;
    }
    
    /* Cards de ação */
    .action-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
    }
    .action-card:hover {
        border-color: #0ea5e9;
        box-shadow: 0 12px 40px rgba(14, 165, 233, 0.12);
        transform: translateY(-2px);
    }
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    .card-description {
        font-size: 0.9rem;
        color: #64748b;
        line-height: 1.6;
    }
    
    /* Stats bar */
    .stats-bar {
        background: linear-gradient(90deg, #f8fafc, #f1f5f9);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        display: flex;
        justify-content: space-around;
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }
    .stat-item {
        text-align: center;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #f8fafc;
    }
    
    /* User badge */
    .user-badge {
        background: linear-gradient(135deg, #0ea5e9, #0284c7);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .user-name {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }
    .user-info {
        font-size: 0.8rem;
        opacity: 0.85;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Features grid */
    .feature-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem 0;
    }
    .feature-icon {
        font-size: 1.2rem;
        min-width: 24px;
    }
    .feature-text {
        font-size: 0.85rem;
        color: #475569;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .action-card {
            background: #1e293b;
            border-color: #334155;
        }
        .card-title { color: #f1f5f9; }
        .card-description { color: #94a3b8; }
        .stats-bar { background: linear-gradient(90deg, #1e293b, #0f172a); border-color: #334155; }
        .stat-number { color: #f1f5f9; }
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Página inicial da aplicação."""

    # Identificação do usuário
    if "usuario" not in st.session_state:
        st.session_state.usuario = None

    if st.session_state.usuario is None:
        # Tela de Login
        st.markdown("""
        <div class="hero-section">
            <div class="hero-title">🏢 PrediALL Facilidades</div>
            <div class="hero-subtitle">Agente Inteligente de Manutenção Predial</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 👤 Acesse o sistema")
        st.caption("Informe seus dados para abrir chamados e acompanhar manutenções.")

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

        if st.button("🔓 Entrar no Sistema", type="primary", use_container_width=True):
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

        # Footer com features
        st.divider()
        st.markdown("""
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; padding: 1rem 0;">
            <div class="feature-item"><span class="feature-icon">⚡</span><span class="feature-text"><strong>Rápido</strong><br>Chamados em menos de 5 min</span></div>
            <div class="feature-item"><span class="feature-icon">🤖</span><span class="feature-text"><strong>IA Integrada</strong><br>Classificação automática</span></div>
            <div class="feature-item"><span class="feature-icon">🔔</span><span class="feature-text"><strong>Notificações</strong><br>Alertas em tempo real</span></div>
            <div class="feature-item"><span class="feature-icon">📊</span><span class="feature-text"><strong>Dashboard</strong><br>KPIs e métricas</span></div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Usuário logado
        usuario = st.session_state.usuario

        # Sidebar
        with st.sidebar:
            st.markdown(f"""
            <div class="user-badge">
                <div class="user-name">👤 {usuario['nome']}</div>
                <div class="user-info">📧 {usuario['email']}<br>🏢 {usuario['unidade']}<br>🔑 {usuario['perfil']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.divider()

            st.markdown("#### 🚨 Emergências")
            st.markdown(
                "**Brigada:** ramal 9999  \n"
                "**SAMU:** 192  \n"
                "**Bombeiros:** 193"
            )
            st.divider()
            if st.button("🚪 Sair do Sistema", use_container_width=True):
                st.session_state.usuario = None
                st.rerun()

        # Header
        st.markdown("""
        <div class="hero-section">
            <div class="hero-title">🏢 PrediALL Facilidades</div>
            <div class="hero-subtitle">Registre, acompanhe e gerencie chamados de manutenção predial</div>
        </div>
        """, unsafe_allow_html=True)

        # Stats resumo
        st.markdown(f"""
        <div class="stats-bar">
            <div class="stat-item"><div class="stat-number">⚡</div><div class="stat-label">&lt; 5 min abertura</div></div>
            <div class="stat-item"><div class="stat-number">🎯</div><div class="stat-label">90% precisão IA</div></div>
            <div class="stat-item"><div class="stat-number">📱</div><div class="stat-label">24/7 disponível</div></div>
            <div class="stat-item"><div class="stat-number">⭐</div><div class="stat-label">4.7/5 satisfação</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Cards de ação
        st.markdown(f"### Olá, {usuario['nome'].split()[0]}! Como posso ajudar?")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="action-card">
                <div class="card-icon">💬</div>
                <div class="card-title">Chat com Agente IA</div>
                <div class="card-description">Descreva o problema em linguagem natural. O agente coleta os dados e abre o chamado automaticamente.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("💬 Iniciar Conversa", type="primary", use_container_width=True, key="btn_chat"):
                st.switch_page("pages/1_💬_Chat_Agente.py")

        with col2:
            st.markdown("""
            <div class="action-card">
                <div class="card-icon">📋</div>
                <div class="card-title">Formulário Rápido</div>
                <div class="card-description">Prefere preencher direto? Use o formulário estruturado para registrar seu chamado em segundos.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📋 Abrir Formulário", use_container_width=True, key="btn_form"):
                st.switch_page("pages/2_📋_Novo_Chamado.py")

        st.markdown("<br>", unsafe_allow_html=True)

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("""
            <div class="action-card">
                <div class="card-icon">📊</div>
                <div class="card-title">Meus Chamados</div>
                <div class="card-description">Acompanhe o status dos seus chamados, veja histórico e avalie o atendimento.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📊 Ver Chamados", use_container_width=True, key="btn_chamados"):
                st.switch_page("pages/3_📊_Meus_Chamados.py")

        with col4:
            if usuario["perfil"] in ["Gestor", "Técnico"]:
                st.markdown("""
                <div class="action-card">
                    <div class="card-icon">📈</div>
                    <div class="card-title">Painel de Gestão</div>
                    <div class="card-description">Dashboard com KPIs, chamados por categoria, SLA, satisfação e visão consolidada.</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("📈 Abrir Painel", use_container_width=True, key="btn_painel"):
                    st.switch_page("pages/4_📈_Painel_Gestor.py")
            else:
                st.markdown("""
                <div class="action-card">
                    <div class="card-icon">💡</div>
                    <div class="card-title">Dicas Rápidas</div>
                    <div class="card-description">
                        • Descreva o problema com detalhes<br>
                        • Informe a localização exata<br>
                        • Anexe fotos se possível<br>
                        • Emergências: ligue ramal 9999
                    </div>
                </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
