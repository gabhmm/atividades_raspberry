const API_BASE = "/api";
let pollingInterval = null;
let currentTargetIP = "";

// Elementos da DOM
const historyEl = document.getElementById("chat-history");
const msgInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const alertEl = document.getElementById("polling-alert");
const timerSpan = document.getElementById("polling-timer");
const partnerIpInput = document.getElementById("partner-ip");
const myGroupInput = document.getElementById("my-group");

// Ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
    fetchHistory();
    // Atualizar histórico a cada 3 segundos pra ver novas msgs
    setInterval(fetchHistory, 3000); 
});

// Permite enviar com a tecla Enter
msgInput.addEventListener("keypress", (e) => {
    if(e.key === "Enter") sendMessage();
});

async function fetchHistory() {
    try {
        const response = await fetch(`${API_BASE}/history`);
        if(response.ok) {
            const messages = await response.json();
            renderMessages(messages);
        }
    } catch (e) {
        console.error("Erro ao carregar histórico", e);
    }
}

function renderMessages(messages) {
    if(messages.length === 0) return;
    
    historyEl.innerHTML = "";
    messages.forEach(msg => {
        const div = document.createElement("div");
        div.className = `message ${msg.is_sent_by_me ? 'sent' : 'received'}`;
        
        const date = new Date(msg.timestamp);
        const timeStr = `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;

        // textContent evita XSS: o conteúdo vem de outros grupos e nunca é interpretado como HTML
        div.append(
            criarSpan("msg-sender", msg.sender),
            criarSpan("msg-content", msg.content),
            criarSpan("msg-time", timeStr)
        );
        historyEl.appendChild(div);
    });

    // Rola para o final
    historyEl.scrollTop = historyEl.scrollHeight;
}

function criarSpan(className, text) {
    const span = document.createElement("span");
    span.className = className;
    span.textContent = text;
    return span;
}

async function sendMessage() {
    const content = msgInput.value.trim();
    currentTargetIP = partnerIpInput.value.trim();
    const senderName = myGroupInput.value.trim() || "Anônimo";

    if(!content || !currentTargetIP) {
        alert("Preencha o IP do parceiro e a mensagem!");
        return;
    }

    // Desabilita input enquanto envia
    msgInput.disabled = true;
    sendBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/send`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                target_ip: currentTargetIP,
                sender: senderName,
                content: content
            })
        });

        if(response.ok) {
            msgInput.value = "";
            fetchHistory(); // Recarrega histórico para mostrar a msg
        } else {
            const errData = await response.json();
            throw new Error(errData.detail || "Erro desconhecido");
        }

    } catch (error) {
        console.error(error);
        // Entra no modo de polling (falha no envio)
        iniciarPolling();
    } finally {
        // Só reabilita se NÃO entrou em modo de polling (senão o polling é desfeito)
        if(pollingInterval === null) {
            msgInput.disabled = false;
            sendBtn.disabled = false;
            msgInput.focus();
        }
    }
}

function iniciarPolling() {
    if(pollingInterval) return; // Já está em polling

    alertEl.classList.remove("hidden");
    let secondsLeft = 15;
    timerSpan.textContent = secondsLeft;

    msgInput.disabled = true;
    sendBtn.disabled = true;

    pollingInterval = setInterval(async () => {
        secondsLeft--;
        timerSpan.textContent = secondsLeft;

        if(secondsLeft <= 0) {
            // Hora de tentar o ping
            try {
                const response = await fetch(`http://${currentTargetIP}/api/ping`, {
                    // Prevenir loop infinito, usa um abort controller se quiser, mas timeout nativo aqui não tem,
                    // porém requisições falhas retornam rápido se a porta estiver fechada.
                });

                if(response.ok) {
                    // Voltou a ficar online!
                    pararPolling();
                    alert("Parceiro Voltou! Conexão Restabelecida.");
                } else {
                    secondsLeft = 15; // reseta timer
                }
            } catch (e) {
                // Continua falhando
                secondsLeft = 15;
            }
        }
    }, 1000);
}

function pararPolling() {
    clearInterval(pollingInterval);
    pollingInterval = null;
    alertEl.classList.add("hidden");
    msgInput.disabled = false;
    sendBtn.disabled = false;
}
