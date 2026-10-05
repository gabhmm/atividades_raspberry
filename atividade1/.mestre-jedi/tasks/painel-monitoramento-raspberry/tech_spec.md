# Technical Specification (TechSpec) - Painel de Monitoramento Raspberry Pi

## 1. Arquitetura e Fluxo de Dados
A aplicação utilizará uma arquitetura cliente-servidor padrão com comunicação via HTTP e REST.

```mermaid
graph TD
    Client[Navegador (Frontend)]
    API[Flask Backend API]
    Sys[Sistema Operacional (Raspberry Pi)]
    
    Client -- "1. GET / (Página Inicial HTML)" --> API
    API -- "2. Retorna index.html" --> Client
    Client -- "3. GET /api/system-status (AJAX polling periódico)" --> API
    API -- "4. Executa rotinas de leitura" --> Sys
    Sys -- "5. Retorna dados brutos (psutil/arquivos linux)" --> API
    API -- "6. Responde com JSON" --> Client
```

## 2. Tecnologias e Bibliotecas
- **Backend:** 
  - `Flask` para o servidor web e roteamento.
  - `psutil` para facilitar a coleta de dados de processador, memória, disco e tempo de atividade (uptime), evitando depender exclusivamente do parsing de arquivos em `/proc`. Alternativamente, a leitura de `/sys/class/thermal/thermal_zone0/temp` pode ser feita para temperatura da CPU (ou `psutil.sensors_temperatures()`).
  - `socket` para obter informações de rede e hostname.
- **Frontend:**
  - HTML5, CSS3, e Vanilla JavaScript (Fetch API para polling assíncrono).

## 3. Modelagem de Dados
Para garantir tipagem estrita no Python (3.12+), utilizaremos `dataclasses` para padronizar as respostas da nossa API:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class SystemStatus:
    hostname: str
    ip_address: str
    uptime_seconds: float
    cpu_usage_percent: float
    cpu_temperature: Optional[float]
    ram_usage_percent: float
    ram_total_mb: float
    disk_usage_percent: float
    disk_total_mb: float
    timestamp: str  # ISO 8601
```

## 4. Endpoints da API

### `GET /`
- **Descrição:** Rota principal que renderiza e serve a interface do usuário.
- **Resposta:** O arquivo `index.html`.

### `GET /api/system-status`
- **Descrição:** Retorna os dados em tempo real da Raspberry Pi.
- **Resposta de Sucesso (200 OK):**
```json
{
  "hostname": "raspberrypi",
  "ip_address": "192.168.1.100",
  "uptime_seconds": 123456.78,
  "cpu_usage_percent": 15.4,
  "cpu_temperature": 45.0,
  "ram_usage_percent": 60.5,
  "ram_total_mb": 4096,
  "disk_usage_percent": 45.2,
  "disk_total_mb": 32000,
  "timestamp": "2026-10-05T20:30:00Z"
}
```
- **Tratamento de Erros:** Caso ocorra erro na leitura de um sensor (como o de temperatura que pode variar se for testado em outro OS local), a API deverá retornar `null` (ou `None` em Python) para aquele campo, evitando que a requisição inteira falhe.

## 5. Frontend Polling
No Frontend (JavaScript), utilizaremos `setInterval` e a API `fetch` para realizar requisições ao `/api/system-status` a cada X segundos (por exemplo, a cada 2 ou 3 segundos) e atualizar os elementos no DOM utilizando `document.getElementById()`.
