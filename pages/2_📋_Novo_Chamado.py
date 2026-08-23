import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database import criar_chamado
from services.notifications import notificar_novo_chamado

st.set_page_config(page_title="Novo Chamado - PrediALL", page_icon="📋", layout="wide")

st.title("📋 Novo Chamado — Formulário Rápido")

# Verificar login
if "usuario" not in st.session_state or st.session_state.usuario is None:
    st.warning("⚠️ Faça login na página inicial para acessar.")
    if st.button("Ir para Login"):
        st.switch_page("app.py")
    st.stop()

usuario = st.session_state.usuario

st.info(f"👤 Solicitante: **{usuario['nome']}** | 🏢 Unidade: **{usuario['unidade']}**")

st.divider()

# Formulário
with st.form("form_chamado", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        local = st.text_input(
            "📍 Local exato *",
            placeholder="Ex.: 4º andar, sala 405 / Doca 03 / Linha de envasamento 02",
            help="Seja específico: andar, sala, setor, linha, galpão"
        )

        tipo_ocorrencia = st.selectbox(
            "🔧 Tipo de Ocorrência *",
            [
                "Selecione...",
                "Elétrica",
                "Climatização / Refrigeração",
                "Hidráulica",
                "Limpeza / Higienização",
                "Mobiliário",
                "Infraestrutura (Docas, Estrutural)",
                "Predial Geral",
            ]
        )

    with col2:
        urgencia = st.selectbox(
            "⚡ Urgência *",
            ["Normal", "Baixa", "Alta", "Crítica"],
            help=(
                "Crítica: risco à segurança ou parada operacional | "
                "Alta: impacto significativo | "
                "Normal: manutenção corretiva | "
                "Baixa: melhoria/preventiva"
            )
        )

        ramal = st.text_input(
            "📞 Ramal para contato",
            value=usuario.get("ramal", ""),
            placeholder="4532"
        )

    descricao = st.text_area(
        "📝 Descrição detalhada *",
        placeholder="Descreva o problema com o máximo de detalhes possível...",
        height=120
    )

    # Upload de foto
    foto = st.file_uploader(
        "📷 Anexar foto (opcional)",
        type=["jpg", "jpeg", "png"],
        help="Tire uma foto do problema para facilitar o diagnóstico"
    )

    # Alerta de emergência
    if urgencia == "Crítica":
        st.warning(
            "⚠️ **Chamado Crítico** — Se houver risco imediato à vida "
            "(gás, incêndio, elétrico grave), ligue AGORA para:\n"
            "- Brigada: ramal 9999\n"
            "- SAMU: 192 | Bombeiros: 193"
        )

    st.divider()
    submitted = st.form_submit_button("✅ Registrar Chamado", type="primary", use_container_width=True)

    if submitted:
        # Validação
        erros = []
        if not local.strip():
            erros.append("Local é obrigatório")
        if tipo_ocorrencia == "Selecione...":
            erros.append("Tipo de Ocorrência é obrigatório")
        if not descricao.strip():
            erros.append("Descrição é obrigatória")

        if erros:
            for erro in erros:
                st.error(f"❌ {erro}")
        else:
            # Criar chamado
            dados = {
                "unidade": usuario["unidade"],
                "local": local.strip(),
                "tipo_ocorrencia": tipo_ocorrencia,
                "urgencia": urgencia,
                "descricao": descricao.strip(),
                "solicitante_nome": usuario["nome"],
                "solicitante_email": usuario["email"],
                "solicitante_ramal": ramal,
                "categoria_ia": tipo_ocorrencia,  # No formulário, o usuário escolhe
                "confianca_ia": 100,  # Certeza total (escolha humana)
                "criado_via": "Formulário",
            }

            resultado = criar_chamado(dados)

            if resultado:
                st.success(
                    f"✅ **Chamado #{resultado['id']} registrado com sucesso!**\n\n"
                    f"📍 {usuario['unidade']} — {local}\n"
                    f"🔧 {tipo_ocorrencia} | ⚡ {urgencia}\n\n"
                    f"Você será notificado sobre atualizações."
                )
                # Notificar equipe
                notificar_novo_chamado(resultado)
            else:
                st.error("❌ Erro ao registrar o chamado. Tente novamente.")
