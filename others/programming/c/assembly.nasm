[BITS 32]

SECTION .data
        global _start
        msg_len equ 16

SECTION .text
        msg db "Deneme Yazisi 2", 10, 0

_start:
        push msg
        call _print
        add esp, 4
        call _exit

_print:
        push ebp
        mov ebp, esp

        mov eax, 4
        mov ebx, 1
        mov ecx, [ebp + 8]
        mov edx, msg_len
        int 80h

        pop ebp
        ret

_exit:
        mov eax, 1
        mov ebx, 0
        int 80h
        ret
