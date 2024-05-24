#!/bin/bash

GITHUB_API_SUBNETS="\
192.30.252.0/22
185.199.108.0/22
140.82.112.0/20
143.55.64.0/20
2a0a:a440::/29
2606:50c0::/32
20.201.28.148/32
20.205.243.168/32
102.133.202.248/32
20.248.137.49/32
20.207.73.85/32
20.27.177.116/32
20.200.245.245/32
20.233.54.49/32"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

while read -r subnet; do
    iptables -A OUTPUT -d "${subnet}" -p tcp -m tcp \
        --dport 22  -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT 2> /dev/null
    iptables -A OUTPUT -d "${subnet}" -p tcp -m tcp \
        --dport 80  -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT 2> /dev/null
    iptables -A OUTPUT -d "${subnet}" -p tcp -m tcp \
        --dport 443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT 2> /dev/null
done <<< "${GITHUB_API_SUBNETS}"

echo "Allow upload configuration done"