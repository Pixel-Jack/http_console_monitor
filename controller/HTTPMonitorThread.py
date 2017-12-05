from scapy.all import *

def receive_callback(x):
    x.show()

rep = sniff(filter="port 80", count=0, prn=lambda x : receive_callback(x))