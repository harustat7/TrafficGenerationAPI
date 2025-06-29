from scapy.all import IP, TCP, UDP, DNS, DNSQR, send, wrpcap, Raw
import random

packets = []

# -------------- APT ATTACKS ----------------

# 1. Initial Compromise (HTTP SYN)
for _ in range(50):
    packets.append(IP(dst="192.168.1.10")/TCP(dport=80, flags="S"))

# 2. Reconnaissance (port scan)
for port in range(20, 30):
    packets.append(IP(dst="192.168.1.11")/TCP(dport=port, flags="S"))

# 3. Lateral Movement (SMB, RDP)
for _ in range(30):
    packets.append(IP(dst="192.168.1.12")/TCP(dport=445, flags="S"))
    packets.append(IP(dst="192.168.1.12")/TCP(dport=3389, flags="S"))

# 4. Pivoting (internal SSH attempts)
for ip in ["192.168.1.13", "192.168.1.14", "192.168.1.15"]:
    packets.append(IP(dst=ip)/TCP(dport=22, flags="S"))

# 5. Data Exfiltration (large UDP)
for _ in range(20):
    packets.append(IP(dst="192.168.1.16")/UDP(dport=53)/Raw("X"*1400))

# -------------- DDOS ATTACKS ----------------

# SYN Flood
for _ in range(100):
    packets.append(IP(dst="192.168.1.20")/TCP(dport=80, flags="S"))

# UDP Flood
for _ in range(100):
    packets.append(IP(dst="192.168.1.20")/UDP(dport=123)/Raw("X"*800))

# UDP-lag
for _ in range(100):
    packets.append(IP(dst="192.168.1.20")/UDP(dport=random.randint(1000, 65535))/Raw("X"*10))

# DrDoS Attacks
# DrDoS_DNS
for _ in range(20):
    packets.append(IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="example.com")))

# DrDoS_NTP
for _ in range(20):
    packets.append(IP(dst="192.168.1.21")/UDP(dport=123)/Raw("\x17\x00\x03\x2a" + "X"*46))

# DrDoS_SSDP
for _ in range(20):
    packets.append(IP(dst="239.255.255.250")/UDP(dport=1900)/Raw("M-SEARCH * HTTP/1.1\r\nST: ssdp:all\r\n"))

# DrDoS_LDAP
for _ in range(20):
    packets.append(IP(dst="192.168.1.22")/UDP(dport=389)/Raw("X"*60))

# DrDoS_MSSQL
for _ in range(20):
    packets.append(IP(dst="192.168.1.23")/UDP(dport=1434)/Raw("X"*60))

# DrDoS_NetBIOS
for _ in range(20):
    packets.append(IP(dst="192.168.1.24")/UDP(dport=137)/Raw("X"*60))

# DrDoS_UDP (CHARGEN port 19)
for _ in range(20):
    packets.append(IP(dst="192.168.1.25")/UDP(dport=19)/Raw("X"*1400))

# Save to PCAP
if __name__ == "__main__":
    wrpcap("complete_attack_traffic.pcap", packets)
    print("✅ Saved to complete_attack_traffic.pcap")

