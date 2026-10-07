from dataclasses import dataclass
from typing import Optional


@dataclass
class Message:
    id: str  # UUID da mensagem
    sender: str
    content: str
    timestamp: str  # Formato ISO 8601 (ex: "2026-10-06T21:07:53Z")
    is_sent_by_me: bool = False  # Para separar visualmente "Enviadas" e "Recebidas" na UI
    target_ip: Optional[str] = None  # Apenas para mensagens enviadas
