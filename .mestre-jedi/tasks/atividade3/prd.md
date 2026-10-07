# Product Requirements Document (PRD) - Chat Local Raspberry Pi

## 1. Visão Geral
**O quê:** Um chat web local que roda em uma Raspberry Pi, acessível via navegador, para troca de mensagens de texto entre diferentes aplicações (grupos) na mesma rede local.
**Por quê:** Para permitir a comunicação assíncrona entre diferentes instâncias do chat criadas por outros grupos, garantindo que as mensagens sejam enviadas com segurança, que o sistema não falhe em caso de indisponibilidade e que um histórico da conversa seja mantido.

## 2. Requisitos Principais (Essenciais)
- Interface web para enviar e visualizar mensagens.
- Consultar separadamente mensagens "Enviadas" e "Recebidas".
- Histórico mantido durante a execução da aplicação (em memória ou arquivo simples).
- Identificar usuário/grupo remetente e informar o endereço de destino (IP/Porta) no envio.
- Visualizar detalhes das mensagens: Remetente, Conteúdo e Horário.
- Notificar o usuário sobre sucesso ou falha no envio.
- Tratamento de falhas: A aplicação não deve "cair" se o destinatário estiver offline.
- Restrição: Bloquear envio de mensagens vazias.
- Resiliência (Polling/Heartbeat): Caso o envio falhe por indisponibilidade do destinatário, a aplicação deve realizar verificações automáticas (polling) a cada 15 segundos para descobrir se ele voltou a ficar online.
- Feedback de Reconexão: A interface deve exibir um contador regressivo (ex: 15s, 14s...) indicando o tempo para a próxima tentativa de conexão, e notificar o usuário assim que o parceiro estiver disponível novamente.

## 3. Contrato de Comunicação (Proposta Inicial)
Para responder diretamente à sua dúvida, proponho que a comunicação entre os grupos siga este formato padrão (simples e direto). Esse contrato deve ser o que você enviará/combinará com os grupos parceiros:

- **Como uma aplicação localizará o chat da outra?** 
  Através do endereço IP local e da porta do servidor do outro grupo (informados manualmente pelo usuário na interface na hora de enviar).
- **Qual endereço (endpoint) será utilizado para receber?**
  - Para receber mensagens: `POST /api/messages`
  - Para verificação de status (Polling/Ping): `GET /api/ping` (Nova rota recomendada para saber se a Raspberry Pi parceira está online).
- **Qual método de comunicação será aceito?**
  `POST` para mensagens e `GET` para o ping de status.
- **Quais informações acompanharão cada mensagem / Estrutura de Dados (JSON)?**
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "sender": "Nome do Seu Grupo",
    "content": "Conteúdo da mensagem de texto",
    "timestamp": "2026-10-06T21:07:53Z"
  }
  ```
- **Como o destinatário informará se a mensagem foi recebida ou rejeitada?**
  Através de códigos de status HTTP:
  - `200 OK` ou `201 Created`: Sucesso (recebida).
  - `400 Bad Request`: Rejeitada (campos faltando, JSON inválido ou mensagem vazia).
  - A resposta pode conter um JSON opcional: `{"status": "success", "message": "Mensagem recebida"}`.
- **Como cada mensagem poderá ser identificada?**
  Pelo campo `id` enviado no JSON (preferencialmente um UUID gerado por quem envia).

## 4. Próximos Passos
Após a aprovação deste PRD, avançaremos para a criação do **TechSpec** (Arquitetura, Stack, Rotas e Armazenamento).
