.global your_asm_fn
.section .text

your_asm_fn:

push    %ebp
mov     %esp,%ebp

# Your code here

push $0xc105ed
mov %esp, %eax

push $str1
push %eax
push $0xacce55ed

call practice

leave
ret

str1:
    .string "coolfood"