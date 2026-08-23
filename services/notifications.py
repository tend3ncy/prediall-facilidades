"""
Serviço de Notificações — Telegram Bot.
Envia alertas para equipe técnica e gestores.
"""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_notificacao(mensagem: str, chat_id: str = None) -> bool:
    """
    Envia uma notificação via Telegram.
    
    Args:
        mensagem: Texto da notificação (suporta Markdown)
        chat_id: ID do chat/grupo (usa padrão se não informado)
    
    Returns:
        True se enviou com sucesso, False caso contrário.
    """
    if not TELEGRAM_BOT_TOKEN:
        print("[NOTIFICAÇÃO - SEM TOKEN] ", mensagem)
        return False

    target_chat = chat_id or TELEGRAM_CHAT_ID
    if not target_chat:
        print("[NOTIFICAÇÃO - SEM CHAT_ID] ", mensagem)
        return False

    try:
        import requests
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": target_chat,
            "text": mensagem,
            "parse_mode": "Markdown",
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"[ERRO NOTIFICAÇÃO] {e}")
        return False


def notificar_novo_chamado(chamado: dict) -> bool:
    """Notifica a equipe sobre um novo chamado."""
    emoji_urgencia = {
        "Crítica": "🚨",
        "Alta": "🔴",
        "Normal": "🟡",
        "Baixa": "🟢",
    }

    emoji = emoji_urgencia.get(chamado.get("urgencia", "Normal"), "📋")

    mensagem = (
        f"{emoji} *NOVO CHAMADO*\n\n"
        f"*ID:* #{chamado.get('id', 'N/A')}\n"
        f"*Tipo:* {chamado.get('tipo_ocorrencia', 'N/A')}\n"
        f"*Urgência:* {chamado.get('urgencia', 'N/A')}\n"
        f"*Unidade:* {chamado.get('unidade', 'N/A')}\n"
        f"*Local:* {chamado.get('local', 'N/A')}\n"
        f"*Descrição:* {chamado.get('descricao', 'N/A')}\n"
        f"*Solicitante:* {chamado.get('solicitante_nome', 'N/A')}\n"
        f"*Via:* {chamado.get('criado_via', 'N/A')}"
    )

    return enviar_notificacao(mensagem)


def notificar_emergencia(chamado: dict) -> bool:
    """Notifica sobre emergência (prioridade máxima)."""
    mensagem = (
        "🚨🚨🚨 *EMERGÊNCIA DETECTADA* 🚨🚨🚨\n\n"
        f"*Unidade:* {chamado.get('unidade', 'N/A')}\n"
        f"*Local:* {chamado.get('local', 'N/A')}\n"
        f"*Tipo:* {chamado.get('tipo_ocorrencia', 'N/A')}\n"
        f"*Descrição:* {chamado.get('descricao', 'N/A')}\n\n"
        "⚠️ *AÇÃO IMEDIATA NECESSÁRIA*\n"
        "Brigada de Incêndio: ramal 9999\n"
        "SAMU: 192 | Bombeiros: 193"
    )

    return enviar_notificacao(mensagem)


def notificar_sla_estourado(chamado: dict) -> bool:
    """Notifica gestor sobre chamado com SLA estourado."""
    mensagem = (
        "⏰ *SLA ESTOURADO*\n\n"
        f"*Chamado:* #{chamado.get('id', 'N/A')}\n"
        f"*Tipo:* {chamado.get('tipo_ocorrencia', 'N/A')}\n"
        f"*Urgência:* {chamado.get('urgencia', 'N/A')}\n"
        f"*Aberto em:* {chamado.get('data_abertura', 'N/A')}\n"
        f"*Local:* {chamado.get('unidade', '')} - {chamado.get('local', '')}\n\n"
        "🔴 Chamado excedeu o prazo de atendimento!"
    )

    return enviar_notificacao(mensagem)
