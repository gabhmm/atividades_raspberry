document.addEventListener('DOMContentLoaded', () => {
    const refreshBtn = document.getElementById('refresh-btn');
    const lastCheckLabel = document.getElementById('last-check');
    
    // Elementos da UI (Configuração)
    const elHostname = document.getElementById('hostname');
    const elInterface = document.getElementById('interface');
    const elState = document.getElementById('state');
    const elIp = document.getElementById('ip');
    const elNetmask = document.getElementById('netmask');
    const elGateway = document.getElementById('gateway');
    const elDns = document.getElementById('dns');
    
    // Container de Pings
    const pingContainer = document.getElementById('ping-container');

    // Função de Busca via API
    const fetchNetworkData = async () => {
        try {
            refreshBtn.classList.add('loading-state');
            refreshBtn.innerText = 'Atualizando...';
            
            const response = await fetch('/api/network');
            if (!response.ok) throw new Error('Falha de comunicação com o back-end');
            
            const data = await response.json();
            updateUI(data);
            
        } catch (error) {
            console.error('Erro ao buscar dados:', error);
            lastCheckLabel.innerText = '⚠️ Erro ao atualizar dados. O sistema tentará novamente.';
        } finally {
            refreshBtn.classList.remove('loading-state');
            refreshBtn.innerText = 'Nova Verificação';
        }
    };

    // Função de Atualização da DOM
    const updateUI = (data) => {
        // Remover classes de skeleton loading
        [elHostname, elInterface, elState, elIp, elNetmask, elGateway, elDns].forEach(el => {
            el.classList.remove('loading');
        });

        elHostname.innerText = data.hostname;
        elInterface.innerText = data.interface;
        
        // Estilização dinâmica do estado da conexão
        elState.innerText = data.connection_state;
        elState.className = 'value badge'; // resetar classes
        if (data.connection_state === 'UP') {
            elState.classList.add('badge-success');
        } else if (data.connection_state === 'DOWN') {
            elState.classList.add('badge-danger');
        } else {
            elState.classList.add('badge-unknown');
        }

        elIp.innerText = data.ip_address;
        elNetmask.innerText = data.netmask;
        elGateway.innerText = data.gateway;
        elDns.innerText = data.dns_servers.join(', ');
        
        lastCheckLabel.innerText = `Última verificação: ${data.last_check_time}`;

        // Renderização dos resultados de Ping
        pingContainer.innerHTML = '';
        data.ping_results.forEach(ping => {
            const card = document.createElement('div');
            card.className = 'ping-card';
            
            let badgeClass = 'badge-unknown';
            if (ping.status === 'Sucesso') badgeClass = 'badge-success';
            if (ping.status === 'Atenção') badgeClass = 'badge-warning';
            if (ping.status === 'Falha') badgeClass = 'badge-danger';

            const timeDisplay = ping.response_time_ms !== null 
                ? `${ping.response_time_ms.toFixed(1)} <span>ms</span>` 
                : 'Falha <span>ms</span>';

            card.innerHTML = `
                <div class="ping-header">
                    <div>
                        <div class="ping-name">${ping.name}</div>
                        <div class="ping-dest">${ping.destination}</div>
                    </div>
                    <span class="badge ${badgeClass}">${ping.status}</span>
                </div>
                <div class="ping-time">${timeDisplay}</div>
                <div class="ping-timestamp">${ping.timestamp}</div>
            `;
            pingContainer.appendChild(card);
        });
    };

    // Eventos e Ações Iniciais
    refreshBtn.addEventListener('click', fetchNetworkData);

    // Primeira requisição ao carregar a página
    fetchNetworkData();

    // POLLING: Atualização automática a cada 10 segundos
    setInterval(fetchNetworkData, 10000);
});
