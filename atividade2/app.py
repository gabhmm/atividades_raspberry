from flask import Flask, jsonify, render_template
from dataclasses import dataclass, asdict
from typing import List, Optional
import subprocess
import socket
import datetime
import re
import os

app = Flask(__name__)

@dataclass
class PingResult:
    destination: str
    name: str
    status: str
    response_time_ms: Optional[float]
    timestamp: str

@dataclass
class NetworkInfo:
    hostname: str
    interface: str
    connection_state: str
    ip_address: str
    netmask: str
    gateway: str
    dns_servers: List[str]
    last_check_time: str
    ping_results: List[PingResult]

def get_hostname() -> str:
    return socket.gethostname()

def get_default_interface_and_gateway() -> tuple[str, str]:
    try:
        # Pega a interface e gateway padrão do `ip route`
        result = subprocess.run(["ip", "-4", "route", "show", "default"], capture_output=True, text=True)
        # Saída esperada: default via 192.168.1.1 dev eth0 ...
        output = result.stdout.strip()
        if output:
            match = re.search(r'default via (\S+) dev (\S+)', output)
            if match:
                return match.group(2), match.group(1)
    except Exception:
        pass
    return "N/A", "N/A"

def get_ip_and_netmask(interface: str) -> tuple[str, str]:
    if interface == "N/A":
        return "N/A", "N/A"
    try:
        result = subprocess.run(["ip", "-4", "addr", "show", interface], capture_output=True, text=True)
        # inet 192.168.1.100/24 brd ...
        output = result.stdout
        match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', output)
        if match:
            ip = match.group(1)
            cidr = int(match.group(2))
            
            # Converte CIDR para mascara (ex: 24 -> 255.255.255.0)
            mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
            netmask = f"{(mask >> 24) & 0xff}.{(mask >> 16) & 0xff}.{(mask >> 8) & 0xff}.{mask & 0xff}"
            return ip, netmask
    except Exception:
        pass
    return "N/A", "N/A"

def get_interface_state(interface: str) -> str:
    if interface == "N/A":
        return "Desconhecido"
    state_file = f"/sys/class/net/{interface}/operstate"
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return f.read().strip().upper()
    return "Desconhecido"

def get_dns_servers() -> List[str]:
    servers = []
    if os.path.exists("/etc/resolv.conf"):
        with open("/etc/resolv.conf", 'r') as f:
            for line in f:
                if line.startswith("nameserver"):
                    parts = line.split()
                    if len(parts) > 1:
                        servers.append(parts[1])
    return servers if servers else ["N/A"]

def run_ping(destination: str, name: str) -> PingResult:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not destination or destination == "N/A":
        return PingResult(destination="N/A", name=name, status="Falha", response_time_ms=None, timestamp=timestamp)
        
    try:
        # Executa 1 ping, espera até 2 segundos
        result = subprocess.run(["ping", "-c", "1", "-W", "2", destination], capture_output=True, text=True)
        if result.returncode == 0:
            # Pega o tempo em ms
            match = re.search(r'time=([\d\.]+)\s*ms', result.stdout)
            if match:
                time_ms = float(match.group(1))
                status = "Atenção" if time_ms >= 50.0 else "Sucesso"
                return PingResult(destination, name, status, time_ms, timestamp)
            return PingResult(destination, name, "Sucesso", None, timestamp)
        else:
            return PingResult(destination, name, "Falha", None, timestamp)
    except Exception:
        return PingResult(destination, name, "Falha", None, timestamp)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/network")
def api_network():
    interface, gateway = get_default_interface_and_gateway()
    ip, netmask = get_ip_and_netmask(interface)
    
    # Destinos de ping requeridos: Gateway, Serviço Local, Serviço Externo
    ping_results = [
        run_ping(gateway, "Gateway Local"),
        run_ping("127.0.0.1", "Serviço Local (Loopback)"),
        run_ping("8.8.8.8", "Serviço Externo (Google DNS)")
    ]
    
    info = NetworkInfo(
        hostname=get_hostname(),
        interface=interface,
        connection_state=get_interface_state(interface),
        ip_address=ip,
        netmask=netmask,
        gateway=gateway,
        dns_servers=get_dns_servers(),
        last_check_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ping_results=ping_results
    )
    
    return jsonify(asdict(info))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
