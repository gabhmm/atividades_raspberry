# Product Requirements Document (PRD) - Painel de Monitoramento Raspberry Pi

## 1. Visão Geral (O Quê)
O projeto consiste em uma aplicação web de monitoramento em tempo real dos recursos de uma Raspberry Pi. A aplicação contará com um back-end desenvolvido em Python utilizando o microframework Flask, e um front-end simples utilizando HTML, CSS e JavaScript (Vanilla). 

## 2. Motivação (Por Quê)
Permitir a visualização rápida e centralizada da saúde e status do sistema operacional da Raspberry Pi através de qualquer dispositivo conectado à mesma rede local, utilizando apenas um navegador web. O objetivo é criar uma interface legível e organizada, que consulte os dados reais diretamente do hardware no momento da requisição, garantindo informações sempre precisas.

## 3. Requisitos Funcionais
O painel de monitoramento deverá apresentar obrigatoriamente, a partir de dados reais e não simulados:
- [ ] **Identificação:** Nome do equipamento (Hostname).
- [ ] **Rede:** Endereço IP local utilizado pela Raspberry Pi.
- [ ] **Uptime:** Tempo de funcionamento contínuo desde a última inicialização.
- [ ] **Processador:** 
  - Percentual de utilização (carga).
  - Temperatura atual.
- [ ] **Memória:** Percentual ou valores brutos de utilização da memória RAM.
- [ ] **Armazenamento:** Percentual ou valores de espaço de disco utilizado/livre.
- [ ] **Sincronização:** Data e horário da última atualização dos dados consultados.

## 4. Requisitos Não Funcionais & Restrições
- **Arquitetura & Execução:** A aplicação deve rodar nativamente dentro da própria Raspberry Pi.
- **Acesso:** Deve possuir interface via web browser e permitir conexão de outros dispositivos na mesma rede local.
- **Tecnologias:** 
  - Back-end: Python 3.12+ (recomendado) e Flask.
  - Front-end: HTML, CSS básico e JavaScript.
- **Atualização:** As informações da tela devem ser atualizadas automaticamente e de forma assíncrona (via requisições AJAX/Fetch) em intervalos regulares, sem a necessidade de recarregar a página (F5).
- **Tratamento de Erros:** O sistema deve tratar falhas e ser resiliente caso alguma informação (ex: temperatura) não possa ser lida pelo sistema operacional, exibindo mensagens apropriadas em vez de "quebrar" a aplicação.
- **Escopo Delimitado:** O projeto **NÃO** deve usar banco de dados, **NÃO** terá sistema de autenticação/login e **NÃO** utilizará APIs ou serviços externos.
