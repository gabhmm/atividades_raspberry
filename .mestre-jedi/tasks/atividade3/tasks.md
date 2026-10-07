# Tasks & Checklist de Execução - Chat Local Raspberry Pi

Este documento é o nosso guia passo a passo. Devemos seguir a ordem abaixo rigorosamente durante a implementação.

## Fase 1: Setup e Fundações
- [x] **Task 1.1:** Criar a estrutura física de pastas dentro de `atividade3/` (`backend/` e `frontend/`).
- [x] **Task 1.2:** Configurar o ambiente virtual Python e criar o arquivo `requirements.txt` (adicionar `fastapi`, `uvicorn`, `requests`).

## Fase 2: Construção do Back-end (FastAPI)
- [x] **Task 2.1:** Criar o arquivo `models.py` contendo a `@dataclass Message`.
- [x] **Task 2.2:** Criar o arquivo `chat_service.py` com a lógica em memória (ou JSON) para armazenar o histórico de mensagens ("Enviadas" e "Recebidas").
- [x] **Task 2.3:** Criar o arquivo `main.py` com o servidor FastAPI.
- [x] **Task 2.4:** Implementar as rotas públicas (Contrato): `POST /api/messages` e `GET /api/ping`.
- [x] **Task 2.5:** Implementar as rotas internas: `GET /api/history` e `POST /api/send` (com a lógica de usar `requests` para bater no IP do parceiro).

## Fase 3: Construção do Front-end (UI/UX)
- [x] **Task 3.1:** Criar o `index.html` com a interface: 
    - Campo de input para IP/Porta do parceiro.
    - Campo para nome do seu grupo.
    - Campo de texto e botão de envio para a mensagem.
    - Área separada para visualizar mensagens enviadas e recebidas.
    - Elemento oculto para exibir o Contador de Reconexão (Polling).
- [x] **Task 3.2:** Criar o `style.css` para deixar visualmente amigável e separar mensagens (ex: balão verde para enviadas, cinza para recebidas).

## Fase 4: Integração Front-end e Polling (JavaScript)
- [x] **Task 4.1:** No `app.js`, implementar a função para carregar o histórico no carregamento da página chamando `GET /api/history`.
- [x] **Task 4.2:** Implementar a lógica de envio (pegar dados da UI e disparar `POST /api/send`).
- [x] **Task 4.3:** Implementar o Polling/Heartbeat: 
    - Capturar erro `503 Service Unavailable` ou falha de fetch.
    - Exibir o timer de 15 segundos na tela.
    - Fazer o `setInterval` bater em `GET /api/ping` no IP do parceiro.
    - Restaurar a UI em caso de `200 OK`.

## Fase 4.5: Correções (Revisão de Código)
> Itens identificados na revisão antes da homologação. ✅ Aprovado e implementado.

- [x] **Task 4.5.1 — Bug do Polling (crítico):** Em `app.js`, impedir que o `finally` de `sendMessage()` reabilite o input/botão quando o modo de polling foi ativado. Reabilitar apenas se `pollingInterval === null`.
- [x] **Task 4.5.2 — Acesso pela rede:** Em `main.py`, trocar `host="127.0.0.1"` por `host="0.0.0.0"` para que as Raspberry Pis dos outros grupos consigam acessar a API. Atualizar o `print` de startup.
- [x] **Task 4.5.3 — Aderência à TechSpec (`@dataclass`):** Reescrever `models.py` usando `from dataclasses import dataclass` com type hints estritos (conforme TechSpec §2). Em `main.py`, trocar `new_message.model_dump()` por `dataclasses.asdict(new_message)`. Converter `SendRequest` também para `@dataclass`. Adicionar type hints faltantes em `chat_service.py` (`-> None`).
- [x] **Task 4.5.4 — Segurança (XSS):** Em `app.js`, montar os balões com `textContent` em vez de interpolar `msg.sender`/`msg.content` no `innerHTML`, já que esses dados vêm de outros grupos.
- [x] **Task 4.5.5 — Depreciação:** Em `main.py`, substituir `datetime.datetime.utcnow()` por `datetime.datetime.now(datetime.timezone.utc)`, mantendo o formato ISO 8601 com sufixo `Z`.

## Fase 5: Testes e Homologação
- [x] **Task 5.1:** Rodar a aplicação (`uvicorn`) localmente e testar o envio para o próprio IP para ver se as duas pontas funcionam.
- [x] **Task 5.2:** Testar o cenário de falha proposital (tentar enviar para uma porta fechada) e validar se o Polling funciona corretamente no Front-end.

> ✅ **Homologação concluída.** Back-end: 11/11 checagens automatizadas (envio local, validações 400/422, falha 503 sem persistir, CORS). Front-end: timer de 15s exibido na falha, reconexão detectada via `GET /api/ping` e envio restabelecido (`POST /api/messages` → 201).

## Fase 6: Migração para WebSockets (Tempo Real)
- [x] **Task 6.1:** Em `chat_service.py`, implementar um ConnectionManager para guardar conexões WebSocket ativas e criar a função `broadcast_message()`.
- [x] **Task 6.2:** Em `chat_service.py`, fazer as rotas que salvam mensagens (recebidas e enviadas com sucesso) chamarem o `broadcast_message()`.
- [x] **Task 6.3:** Em `main.py`, adicionar a rota WebSocket (`@app.websocket("/api/ws")`) para aceitar conexões do Front-end. Adicionar biblioteca `websockets` no `requirements.txt`.
- [x] **Task 6.4:** No Front-end (`app.js`), remover o `setInterval(fetchHistory, 3000)` e iniciar uma conexão com `new WebSocket()`. Configurar o evento `onmessage` para criar e renderizar o balão da nova mensagem recebida em tempo real.
