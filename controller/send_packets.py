from scapy.all import *

ip = IP(src="192.168.1.114")
ip.dst="192.168.1.25"

tcp=TCP(sport=1025, dport=80)

for i in range(10):
    send(ip/tcp)
    time.sleep(2)