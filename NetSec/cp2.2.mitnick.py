from scapy.all import *

import sys

if __name__ == "__main__":
    conf.iface = sys.argv[1]
    target_ip = sys.argv[2]
    trusted_host_ip = sys.argv[3]

    my_ip = get_if_addr(sys.argv[1])

    #TODO: figure out SYN sequence number pattern

    #TODO: TCP hijacking with predicted sequence number
