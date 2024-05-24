.global _main
.section .text

shellcode:
    .asciz "/bin/sh"

_main:

push    %ebp
mov     %esp,%ebp

# Your code here

push $shellcode
push $0

movl $11, %eax

movl $shellcode, %ebx
leal -8(%ebp), %ecx
movl $0, %edx  
                     
int  $0x80 

leave
ret
