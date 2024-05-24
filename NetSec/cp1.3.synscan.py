from scapy.all import *

import sys

def debug(s):
    print('#{0}'.format(s))
    sys.stdout.flush()

if __name__ == "__main__":
    conf.iface = sys.argv[1]
    ip_addr = sys.argv[2]

    my_ip = get_if_addr(sys.argv[1])
    
    src_port = RandShort()
    for dst_port in range(1025):
        
        stealth_scan_resp = sr1(IP(src=my_ip, dst=ip_addr)/TCP(sport=src_port,dport=dst_port,flags="S"), iface=conf.iface, verbose=False, timeout=5)
        if(stealth_scan_resp is None):
            pass
        elif(stealth_scan_resp.haslayer(TCP)):
            if(stealth_scan_resp.getlayer(TCP).flags == 0x12):
                send_rst = sr(IP(src=my_ip, dst=ip_addr)/TCP(sport=src_port,dport=dst_port,flags="R"), iface=conf.iface, verbose=False, timeout=5)
                print(f'{ip_addr}, {dst_port}')
            elif (stealth_scan_resp.getlayer(TCP).flags == 0x14):
                pass
