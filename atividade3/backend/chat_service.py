from models import Message

class ChatService:
    def __init__(self) -> None:
        # Armazena as mensagens em memória durante a execução
        self.history: list[Message] = []

    def save_message(self, message: Message) -> None:
        self.history.append(message)

    def get_history(self) -> list[Message]:
        return self.history

# Instância global para ser usada nas rotas
chat_service_instance = ChatService()
