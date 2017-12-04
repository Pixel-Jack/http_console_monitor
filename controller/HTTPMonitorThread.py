from threading import Thread

from scapy.all import *

sniff(filter="port 80", count=0, prn=None, lfilter=None, timeout=None)