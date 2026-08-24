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

# Inicializar histórico do chat
if "mensagens_chat" not in st.session_state:
    st.session_state.mensagens_chat = []

if "historico_groq" not in st.session_state:
    st.session_state.historico_groq = []

if "chamado_criado" not in st.session_state:
    st.session_state.chamado_criado = False

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = None


def resetar_chat():
    """Limpa o chat para uma nova conversa."""
    st.session_state.mensagens_chat = []
    st.session_state.historico_groq = []
    st.session_state.chamado_criado = False
    st.session_state.system_prompt = None


# Sidebar com informações
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


# Exibir mensagens do histórico
for msg in st.session_state.mensagens_chat:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Mensagem inicial do agente
if not st.session_state.mensagens_chat:
    saudacao = f"Olá, {usuario['nome'].split()[0]}! 👋 Sou o assistente de Facilities. Como posso ajudar você hoje? Descreva o problema que você está enfrentando."
    st.session_state.mensagens_chat.append({"role": "assistant", "content": saudacao})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(saudacao)

# Se chamado já foi criado, mostrar mensagem de sucesso
if st.session_state.chamado_criado:
    st.success("✅ Chamado registrado com sucesso! Use o menu lateral para iniciar uma nova conversa.")
    st.stop()

# Input do usuário
if prompt := st.chat_input("Descreva seu problema..."):
    # Mostrar mensagem do usuário
    st.session_state.mensagens_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Processar com o agente
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analisando..."):
            try:
                # Inicializar system prompt se necessário
                if st.session_state.system_prompt is None:
                    contexto = buscar_contexto(prompt)
                    st.session_state.system_prompt = criar_agente(
                        nome_usuario=usuario["nome"],
                        unidade_usuario=usuario["unidade"],
                        contexto_rag=contexto,
                    )

                # Enviar mensagem ao Groq
                resposta = enviar_mensagem(
                    st.session_state.system_prompt,
                    st.session_state.historico_groq,
                    prompt
                )

                # Atualizar histórico do Groq
                st.session_state.historico_groq.append(
                    {"role": "user", "content": prompt}
                )
                st.session_state.historico_groq.append(
                    {"role": "assistant", "content": resposta}
                )

                # Verificar se é emergência
                if verificar_emergencia(resposta):
                    resposta_limpa = resposta.split('{"emergencia"')[0].strip()
                    st.markdown(resposta_limpa)
                    st.session_state.mensagens_chat.append(
                        {"role": "assistant", "content": resposta_limpa}
                    )
                    notificar_emergencia({
                        "unidade": usuario["unidade"],
                        "local": "Informado no chat",
                        "tipo_ocorrencia": "EMERGÊNCIA",
                        "descricao": prompt,
                    })
                    st.error("🚨 Emergência notificada à equipe de segurança!")

                # Verificar se dados estão completos
                elif dados := extrair_dados_chamado(resposta):
                    # Limpar JSON da resposta para exibição
                    resposta_limpa = resposta
                    if "```json" in resposta_limpa:
                        resposta_limpa = resposta_limpa.split("```json")[0].strip()
                    elif '{"completo"' in resposta_limpa:
                        resposta_limpa = resposta_limpa.split('{"completo"')[0].strip()

                    st.markdown(resposta_limpa)
                    st.session_state.mensagens_chat.append(
                        {"role": "assistant", "content": resposta_limpa}
                    )

                    # Criar chamado no banco
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
                        st.success(
                            f"✅ **Chamado #{resultado['id']} criado com sucesso!**\n\n"
                            f"Você pode acompanhar o status na página 'Meus Chamados'."
                        )
                        notificar_novo_chamado(resultado)
                        st.session_state.chamado_criado = True
                    else:
                        st.error("Erro ao criar chamado. Tente novamente.")

                else:
                    # Resposta normal (ainda coletando dados)
                    st.markdown(resposta)
                    st.session_state.mensagens_chat.append(
                        {"role": "assistant", "content": resposta}
                    )

            except Exception as e:
                erro_msg = f"Desculpe, tive um problema técnico. Tente novamente ou use o formulário. Erro: {str(e)}"
                st.error(erro_msg)
                st.session_state.mensagens_chat.append(
                    {"role": "assistant", "content": erro_msg}
                )
