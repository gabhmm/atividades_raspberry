from dataclasses import asdict, dataclass
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import requests
import datetime
import uuid

from models import Message
from chat_service import chat_service_instance

app = FastAPI(title="Chat Local Raspberry Pi")

# Liberar CORS para o Front-end local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ROTAS PÚBLICAS (O CONTRATO) ===

@app.post("/api/messages", status_code=201)
def receive_message(message: Message, background_tasks: BackgroundTasks):
    """
    Rota que os outros grupos vão chamar para nos enviar uma mensagem.
    """
    if not message.content.strip() or not message.sender.strip():
        raise HTTPException(status_code=400, detail="Remetente ou conteúdo vazio não permitidos.")
    
    # Garantir que quem recebe não trate como "enviada por mim"
    message.is_sent_by_me = False
    
    chat_service_instance.save_message(message)
    # Task 6.2: Envia a mensagem recebida para todos os front-ends conectados via WebSocket
    background_tasks.add_task(chat_service_instance.manager.broadcast, message)
    
    return {"status": "success", "message": "Mensagem recebida"}


@app.get("/api/ping", status_code=200)
def ping():
    """
    Rota de Heartbeat para o parceiro saber que estamos online.
    """
    return {"status": "online"}


# === ROTAS INTERNAS (PARA NOSSO FRONT-END) ===

@app.get("/api/history", response_model=list[Message])
def get_history():
    """
    Retorna todo o histórico de mensagens para desenhar a tela inicial.
    """
    return chat_service_instance.get_history()


@dataclass
class SendRequest:
    target_ip: str
    sender: str
    content: str

@app.post("/api/send", status_code=200)
def send_message(payload: SendRequest, background_tasks: BackgroundTasks) -> dict[str, str]:
    """
    Nosso Front-end chama essa rota para enviar uma mensagem para fora.
    """
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Mensagem vazia")

    # 1. Monta a mensagem que será salva e enviada
    new_message = Message(
        id=str(uuid.uuid4()),
        sender=payload.sender,
        content=payload.content,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        is_sent_by_me=True,
        target_ip=payload.target_ip
    )

    # 2. Tenta fazer a requisição HTTP para a Raspberry Pi do parceiro
    target_url = f"http://{payload.target_ip}/api/messages"
    
    try:
        # Envia como JSON (asdict converte a dataclass em dicionário)
        response = requests.post(
            target_url, 
            json=asdict(new_message),
            timeout=5 # 5 segundos de timeout para não travar muito tempo
        )
        response.raise_for_status() # Lança exceção se não for 200/201
    except requests.exceptions.RequestException as e:
        # 3. Se der erro (ex: Timeout, Connection Refused), avisamos o Front-end
        raise HTTPException(status_code=503, detail=f"Falha ao enviar para o parceiro: {str(e)}")

    # 4. Se deu tudo certo, salva no nosso histórico
    chat_service_instance.save_message(new_message)
    # Task 6.2: Envia a nossa própria mensagem enviada para o Front-end via WebSocket
    background_tasks.add_task(chat_service_instance.manager.broadcast, new_message)
    
    return {"status": "success", "message": "Mensagem enviada com sucesso"}

# Task 6.3: Rota do WebSocket
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await chat_service_instance.manager.connect(websocket)
    try:
        while True:
            # Mantém a conexão aberta esperando mensagens do cliente 
            # (embora nosso cliente só receba, precisamos deste loop para manter vivo)
            await websocket.receive_text()
    except WebSocketDisconnect:
        chat_service_instance.manager.disconnect(websocket)

# === FRONT-END ESTÁTICO ===
import os
from fastapi.staticfiles import StaticFiles

frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    
    print("="*50)
    print("Iniciando o Back-end do Chat Local...")
    print("Servidor escutando em todas as interfaces (0.0.0.0)")
    print("Acesso local: http://127.0.0.1:8000")
    print("Acesso pela rede: http://<IP_DESTA_MAQUINA>:8000")
    print("Aguarde as mensagens de startup do Uvicorn logo abaixo...")
    print("="*50)
    
    # Iniciamos o uvicorn programaticamente.
    # host="0.0.0.0" permite que as Raspberry Pis dos outros grupos alcancem esta API.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
