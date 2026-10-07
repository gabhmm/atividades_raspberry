from dataclasses import asdict
from fastapi import WebSocket
from models import Message

class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Message) -> None:
        # asdict converte a dataclass para dict, e o fastapi converte para JSON
        msg_dict = asdict(message)
        for connection in self.active_connections:
            await connection.send_json(msg_dict)

class ChatService:
    def __init__(self) -> None:
        # Armazena as mensagens em memória durante a execução
        self.history: list[Message] = []
        self.manager = ConnectionManager()

    def save_message(self, message: Message) -> None:
        self.history.append(message)

    def get_history(self) -> list[Message]:
        return self.history

# Instância global para ser usada nas rotas
chat_service_instance = ChatService()
