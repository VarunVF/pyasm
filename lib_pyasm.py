printRAX = ("""
_printRAX:
    push rax                ; save the address of the first char
    xor rbx, rbx            ; count string length in rbx
__printRAXLoop:
    mov cl, [rax]           ; read chars into rcx
    inc rax                 ; point to the next char
    inc rbx                 ; count chars
    cmp cl, 0               ; compare this char to the null char
    jne __printRAXLoop
    
    ; print the string
    mov rax, 1              ; sys_write
    mov rdi, 1              ; stdout
    pop rsi                 ; load the address of the first char
    mov rdx, rbx            ; string length (number of bytes to read)
    syscall
    ret
""")

sys_exit_0 = ("""
_sys_exit:
    mov rax, 60             ; sys_exit
    xor rdi, rdi            ; exit code 0
    syscall
    ret
""")
