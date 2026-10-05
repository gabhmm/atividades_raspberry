# Checklist de Execução (Tasks) - Painel de Monitoramento Raspberry Pi

## Fase 1: Setup e Infraestrutura
- [ ] 1. Criar e configurar o ambiente virtual do Python (opcional, dependendo do setup global na Pi, mas recomendado).
- [ ] 2. Criar o arquivo `requirements.txt` incluindo `Flask` e `psutil`.
- [ ] 3. Instalar as dependências do `requirements.txt`.
- [ ] 4. Criar a estrutura base de pastas:
  - `app.py`
  - `templates/index.html`
  - `static/css/style.css`
  - `static/js/app.js`

## Fase 2: Lógica Backend (Python)
- [ ] 5. Criar um arquivo separado (ou camada dedicada) para os utilitários de monitoramento (`monitor.py`).
- [ ] 6. Criar a `dataclass` `SystemStatus` para forte tipagem dos retornos.
- [ ] 7. Implementar a lógica para obter:
  - Hostname e IP.
  - Tempo de Uptime.
  - CPU: Carga (%) e Temperatura. Tratamento caso temperatura seja `None`.
  - RAM: % uso e Total.
  - Disco: % uso e Total.
- [ ] 8. Implementar no `app.py` a rota `/api/system-status` retornando o objeto em formato JSON.
- [ ] 9. Implementar no `app.py` a rota `/` retornando a renderização do `index.html`.

## Fase 3: Desenvolvimento Frontend (HTML/CSS/JS)
- [ ] 10. Desenvolver a estrutura HTML do painel em `index.html`, utilizando classes semânticas.
- [ ] 11. Estilizar com `style.css` garantindo um visual *premium*, legível e com excelente UI/UX (conforme diretrizes de design, evitando cores puras de sistema).
- [ ] 12. Desenvolver o script `app.js` utilizando `setInterval` e a API `fetch()` para realizar a chamada AJAX para o `/api/system-status`.
- [ ] 13. Mapear o JSON retornado para atualizar os valores de cada elemento HTML.

## Fase 4: Validação
- [ ] 14. Executar a aplicação (Flask run).
- [ ] 15. Validar o acesso pelo navegador.
- [ ] 16. Garantir que, quando valores como Temperatura não estiverem disponíveis, o front-end mostre algo amigável (como "N/A" ou "Sensor Indisponível") ao invés de quebrar.
