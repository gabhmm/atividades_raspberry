# Product Requirements Document (PRD) - Monitor de Rede Raspberry Pi

## 1. Visão Geral e "O Quê"
A aplicação web visa monitorar e exibir a configuração de rede e o status de conectividade de uma Raspberry Pi. O sistema será composto por um back-end que coleta informações reais do sistema operacional e um front-end acessível via navegador para apresentar os resultados de forma clara, moderna e visualmente intuitiva.

## 2. Objetivos e "Por Quê"
- **Diagnóstico Rápido:** Prover visibilidade instantânea da configuração de rede da Raspberry Pi (IP, Gateway, DNS, etc.) sem a necessidade de comandos no terminal.
- **Validação de Conectividade:** Executar testes ativos para destinos chaves (Gateway, rede local, internet) ajudando a isolar e diagnosticar problemas de rede.
- **Conformidade com a Demanda:** Atender a todos os requisitos da "Atividade 2", garantindo execução nativa na Raspberry e experiência de usuário premium.

## 3. Requisitos Essenciais
- **Informações do Equipamento (Monitor):**
  - Nome do equipamento (Hostname).
  - Interface de rede ativa (ex: eth0, wlan0).
  - Tipo ou estado da conexão (ex: UP, DOWN).
  - Endereço IP da Raspberry Pi.
  - Máscara da rede.
  - Endereço do gateway.
  - Servidores DNS configurados.
  - Data e horário da última verificação.

- **Testes de Conectividade (Ping):**
  - **Gateway:** O gateway da rede local.
  - **Serviço Local:** Outro equipamento ou serviço (ex: IP do servidor local ou o próprio localhost para validação de pilha).
  - **Serviço Externo:** Um endereço externo consolidado (ex: `8.8.8.8` ou `google.com`).

- **Dados por Destino Testado:**
  - Endereço ou nome do destino.
  - Estado da comunicação (Sucesso, Atenção, Falha).
  - Tempo aproximado de resposta (ms).
  - Momento em que o teste foi realizado.

- **Comportamento e UI/UX:**
  - Execução direta e leve na Raspberry Pi (Back-end em Python).
  - Acesso via navegador da web.
  - Ação manual para solicitar nova verificação.
  - Diferenciação visual clara: **Verde** (Sucesso), **Amarelo** (Atenção/Lentidão), **Vermelho** (Falha).
  - Sistema resiliente: se um destino falhar, a aplicação continua operando e exibe a falha isolada.
  - Comportamento passivo/ativo pontual: apenas testes pontuais solicitados, sem varreduras na rede (sem interferência).

## 4. Desafios Adicionais
- Atualização automática dos resultados via polling periódico da interface, garantindo a exibição de dados atualizados sem reload manual.

---
**Aprovação Necessária:**
Por favor, revise os requisitos acima. Caso esteja de acordo com o PRD, confirmaremos para avançar à etapa de **TechSpec (Especificação Técnica)**.
