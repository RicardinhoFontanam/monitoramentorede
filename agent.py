import psutil
import speedtest
import requests
import socket
import netifaces as ni
from scapy.all import ARP, Ether, srp
import platform

# =================== CONFIGURAÇÕES ===================
BACKEND_URL = "http://localhost:3000/api/send-data"  # Alterar em produção
TOKEN = "seu-token-aqui"  # Token de autenticação
INTERFACE = "Ethernet"  # ou "Wi-Fi", dependendo da rede

# =================== FUNÇÕES ===================

def medir_banda():
    try:
        st = speedtest.Speedtest()
        download = st.download() / 1_000_000  # Mbps
        return f"{round(download, 2)} Mbps"
    except:
        return "Erro ao medir"

def dispositivos_rede():
    dispositivos = []
    try:
        target_ip = ni.ifaddresses(INTERFACE)[ni.AF_INET][0]['addr'] + '/24'
        arp = ARP(pdst=target_ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp
        result = srp(packet, timeout=3, verbose=0)[0]

        for sent, received in result:
            hostname = received.psrc
            dispositivos.append({"name": hostname, "ip": received.psrc})
    except:
        dispositivos.append({"name": "Erro ao escanear", "ip": "?"})
    return dispositivos

def info_roteador():
    return {"model": "Detectar automaticamente (placeholder)"}

def info_switch():
    return {"model": "Detectar automaticamente (placeholder)", "ports": 8}

def rede_estavel():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

# =================== EXECUÇÃO ===================

def coletar_dados():
    return {
        "token": TOKEN,
        "bandwidth": medir_banda(),
        "stable": rede_estavel(),
        "devices": dispositivos_rede(),
        "router": info_roteador(),
        "switch": info_switch()
    }

def enviar_dados():
    dados = coletar_dados()
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        res = requests.post(BACKEND_URL, json=dados, headers=headers)
        print("Resposta do servidor:", res.status_code, res.text)
    except Exception as e:
        print("Erro ao enviar dados:", str(e))

if __name__ == "__main__":
    enviar_dados()
