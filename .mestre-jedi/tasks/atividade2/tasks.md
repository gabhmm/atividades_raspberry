# Tasks - Monitor de Rede Raspberry Pi

## 1. Configuração do Projeto
- [ ] Criar o arquivo `requirements.txt` contendo `Flask`.
- [ ] Estruturar as pastas padrão do Flask: `templates/` para o HTML e `static/` para os arquivos CSS e JS.
- [ ] Criar o esqueleto do arquivo `app.py` com as definições das `dataclasses`.

## 2. Implementação do Back-end (Python/Linux)
- [ ] Implementar funções utilitárias para coleta de dados do SO:
  - [ ] `get_hostname()`
  - [ ] `get_default_interface_and_gateway()` via `ip route`
  - [ ] `get_ip_and_netmask(interface)` via `ip addr`
  - [ ] `get_dns_servers()` lendo `/etc/resolv.conf`
  - [ ] `get_interface_state(interface)` lendo `/sys/class/net/...`
- [ ] Implementar a função utilitária `run_ping(destino)` para executar ping e fazer o parse do tempo de resposta.
- [ ] Implementar o endpoint principal `GET /api/network` agregando todos os dados na classe `NetworkInfo` e retornando-os como JSON.
- [ ] Implementar o endpoint raiz `GET /` para servir a página HTML.

## 3. Implementação do Front-end (UI/UX)
- [ ] **HTML (`templates/index.html`)**: Estruturar os cards para exibir as informações de rede e a tabela/cards para o resultado do Ping.
- [ ] **CSS (`static/style.css`)**: Implementar o design premium (Glassmorphism, fontes modernas, variáveis de cores CSS).
  - [ ] Definir cores para estados: Verde (Sucesso), Amarelo (Atenção), Vermelho (Falha).
- [ ] **JS (`static/script.js`)**: 
  - [ ] Implementar a chamada assíncrona com `fetch('/api/network')`.
  - [ ] Mapear o JSON recebido atualizando os elementos do DOM.
  - [ ] Implementar o **polling**, configurando a função de `setInterval` para executar a requisição a cada 5~10 segundos.

## 4. Testes e Ajustes
- [ ] Instalar as dependências e iniciar a aplicação (`python3 app.py`).
- [ ] Validar a extração das métricas localmente no ambiente Linux.
- [ ] Ajustar o parsing das strings de saída de sistema caso o SO base tenha formatações distintas.

---
**Aprovação Necessária:**
Mestre, o plano de execução está detalhado e dividido em etapas modulares. **Você aprova as Tasks?** Com seu "sim", começarei a escrever o código rigorosamente seguindo este planejamento (sem Vibe Coding!).
