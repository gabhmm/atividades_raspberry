# Technical Specification (Tech Spec) - Chat Local Raspberry Pi

## 1. Stack Tecnológica
- **Back-end:** Python 3.12+ com **FastAPI** (ou Flask). FastAPI é recomendado por suportar tipagem estrita e **WebSockets** nativamente. O servidor rodará via `uvicorn` e também servirá o Front-end estático.
- **Front-end:** Vanilla HTML, CSS e JavaScript puro (sem frameworks pesados). O consumo das APIs será feito nativamente com a `Fetch API` e atualizações em tempo real com a `WebSocket API`.
- **Armazenamento:** Memória (listas nativas em Python) para salvar o histórico das mensagens (garantindo que não se perca se a página for recarregada).

## 2. Modelagem de Dados (Entidades)
Seguindo as diretrizes do Mestre Jedi, utilizaremos tipagem estrita e `dataclasses` em Python para modelar nossas informações de forma limpa.

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Message:
    id: str  # UUID da mensagem
    sender: str
    content: str
    timestamp: str  # Formato ISO 8601 (ex: "2026-10-06T21:07:53Z")
    is_sent_by_me: bool # Para separar visualmente "Enviadas" e "Recebidas" na UI
    target_ip: Optional[str] = None # Apenas para mensagens enviadas
```

## 3. Arquitetura de Pastas (Proposta)
```text
atividade3/
│
├── backend/
│   ├── main.py           # Configuração do FastAPI e rotas
│   ├── models.py         # As Dataclasses (Message)
│   └── chat_service.py   # Lógica de salvar histórico e encaminhar requisições
│
├── frontend/
│   ├── index.html        # Estrutura e Interface do Chat
│   ├── style.css         # Estilos Visuais (com classes de Enviado/Recebido)
│   └── app.js            # Lógica de tela, Fetch API e Polling/Heartbeat
│
└── requirements.txt      # Dependências (fastapi, uvicorn, requests)
```

## 4. Design das APIs (Endpoints do nosso Back-end)

O back-end servirá dois propósitos: Atender o *nosso* Front-end (UI) e atender as requisições *das outras* Raspberry Pis.

### A) Endpoints Públicos (O Contrato - para os outros grupos acessarem):
- **`POST /api/messages`**: Rota que o outro grupo acessará para nos mandar uma mensagem. Salva a mensagem no histórico como "Recebida" e retorna `200 OK`.
- **`GET /api/ping`**: Rota leve que o outro grupo pode bater para saber se estamos online. Retorna `{"status": "online"}`.

### B) Endpoints Internos (Para o nosso Front-end acessar):
- **`GET /api/history`**: Retorna a lista de todas as mensagens (enviadas e recebidas) para desenhar a tela inicial ao carregar a página.
- **`POST /api/send`**: Rota interna. Nosso Front-end manda a mensagem para o nosso Back-end, junto com o IP de destino. O Back-end salva a mensagem como "Enviada", e faz um HTTP POST via biblioteca `requests` para o IP do outro grupo. Se falhar, o Back-end avisa o Front-end.
- **`ws /api/ws`**: Conexão WebSocket mantida aberta pelo Front-end. Assim que uma nova mensagem chega em `POST /api/messages` ou é enviada com sucesso em `POST /api/send`, o servidor faz o "push" (broadcast) dessa nova mensagem via WebSocket para o Front-end, eliminando o delay.

## 5. Arquitetura de Resiliência (Polling/Heartbeat)
- **Cenário Normal:** Front-end -> `POST /api/send` -> Nosso Back-end -> `POST /api/messages` no IP do Parceiro -> OK.
- **Cenário de Falha:** IP do Parceiro está offline. O nosso `requests.post` falha (Timeout). O Back-end retorna erro 503 (Service Unavailable) para o nosso Front-end.
- **Ação no Front-end:**
  - O `app.js` entra em `estado de reconexão`.
  - Exibe o Timer visual para o usuário.
  - Inicia um `setInterval` a cada 15s.
  - A cada 15s, dispara um `fetch(http://<IP_DO_PARCEIRO>/api/ping)`.
  - Quando o fetch retornar `200 OK`, o `app.js` limpa o timer, notifica o usuário ("Conexão Restabelecida") e libera o botão de enviar.
