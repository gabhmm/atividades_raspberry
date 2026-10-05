const POLL_INTERVAL = 3000; // Atualiza a cada 3 segundos

// Função auxiliar para formatar tempo (segundos para dias, horas, mins)
function formatUptime(totalSeconds) {
    const days = Math.floor(totalSeconds / 86400);
    totalSeconds %= 86400;
    const hours = Math.floor(totalSeconds / 3600);
    totalSeconds %= 3600;
    const minutes = Math.floor(totalSeconds / 60);

    let result = [];
    if (days > 0) result.push(`${days}d`);
    if (hours > 0 || days > 0) result.push(`${hours}h`);
    result.push(`${minutes}m`);

    return result.join(' ');
}

// Atualizar barras de progresso com cores baseadas no percentual
function updateProgressBar(elementId, value) {
    const bar = document.getElementById(elementId);
    if (!bar) return;
    
    bar.style.width = `${value}%`;
    
    // Graduação de cor (verde -> amarelo -> vermelho)
    if (value < 60) {
        bar.style.backgroundColor = 'var(--success)';
    } else if (value < 85) {
        bar.style.backgroundColor = 'var(--warning)';
    } else {
        bar.style.backgroundColor = 'var(--danger)';
    }
}

// Formatar timestamp para hora legível
function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString('pt-BR');
}

// Fetch dos dados da API
async function fetchSystemData() {
    try {
        const response = await fetch('/api/system-status');
        if (!response.ok) throw new Error('Erro na rede');
        
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Falha ao buscar dados do sistema:', error);
        document.getElementById('last-update').textContent = "Desconectado";
        document.querySelector('.pulse').style.backgroundColor = 'var(--danger)';
        document.querySelector('.pulse').style.animation = 'none';
    }
}

// Atualizar DOM
function updateDashboard(data) {
    // Cabeçalho
    document.getElementById('hostname').textContent = `Host: ${data.hostname}`;
    document.getElementById('last-update').textContent = `Atualizado: ${formatTime(data.timestamp)}`;
    document.querySelector('.pulse').style.backgroundColor = 'var(--success)';
    document.querySelector('.pulse').style.animation = 'pulse-animation 2s infinite';

    // Valores
    document.getElementById('ip-address').textContent = data.ip_address;
    document.getElementById('uptime').textContent = formatUptime(data.uptime_seconds);
    
    // CPU
    document.getElementById('cpu-usage').textContent = data.cpu_usage_percent.toFixed(1);
    updateProgressBar('cpu-bar', data.cpu_usage_percent);
    
    if (data.cpu_temperature !== null) {
        document.getElementById('cpu-temp').textContent = data.cpu_temperature.toFixed(1);
    } else {
        document.getElementById('cpu-temp').textContent = "N/A";
    }

    // RAM
    document.getElementById('ram-usage').textContent = data.ram_usage_percent.toFixed(1);
    document.getElementById('ram-total').textContent = Math.round(data.ram_total_mb);
    updateProgressBar('ram-bar', data.ram_usage_percent);

    // Disco
    document.getElementById('disk-usage').textContent = data.disk_usage_percent.toFixed(1);
    document.getElementById('disk-total').textContent = Math.round(data.disk_total_mb);
    updateProgressBar('disk-bar', data.disk_usage_percent);
}

// Iniciar polling
document.addEventListener('DOMContentLoaded', () => {
    fetchSystemData(); // Chamada inicial imediata
    setInterval(fetchSystemData, POLL_INTERVAL);
});
