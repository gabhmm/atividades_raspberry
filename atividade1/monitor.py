import psutil
import socket
import time
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

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
    timestamp: str

def get_system_status() -> SystemStatus:
    # Hostname and IP
    hostname = socket.gethostname()
    try:
        # Pega o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        ip_address = socket.gethostbyname(hostname)

    # Uptime
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time

    # CPU
    cpu_usage_percent = psutil.cpu_percent(interval=0.1)
    
    # Temperatura da CPU (Raspberry Pi específica, trata exceção em outros SOs)
    cpu_temperature = None
    try:
        # Acesso comum na Raspberry
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            cpu_temperature = float(f.read()) / 1000.0
    except (FileNotFoundError, ValueError):
        # Fallback usando psutil se disponível
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.current is not None:
                            cpu_temperature = entry.current
                            break
                    if cpu_temperature is not None:
                        break

    # Memória
    mem = psutil.virtual_memory()
    ram_usage_percent = mem.percent
    ram_total_mb = mem.total / (1024 * 1024)

    # Disco
    disk = psutil.disk_usage('/')
    disk_usage_percent = disk.percent
    disk_total_mb = disk.total / (1024 * 1024)

    # Timestamp
    now_iso = datetime.now(timezone.utc).isoformat()

    return SystemStatus(
        hostname=hostname,
        ip_address=ip_address,
        uptime_seconds=uptime_seconds,
        cpu_usage_percent=cpu_usage_percent,
        cpu_temperature=cpu_temperature,
        ram_usage_percent=ram_usage_percent,
        ram_total_mb=ram_total_mb,
        disk_usage_percent=disk_usage_percent,
        disk_total_mb=disk_total_mb,
        timestamp=now_iso
    )
