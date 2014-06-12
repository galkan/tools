[BITS 32]

SECTION .data
        msg db "%d", 10, 0

SECTION .text
        global main


main:
        mov eax, 10
        mov ebx, 20
        mov ecx, 40

        call AddProc
        push eax
        call _Yazdir
        add esp, 4

        mov eax, 1
        mov ebx, 5
        int 80h


_Yazdir:
        push ebp
        mov ebp, esp

        mov eax, 4
        mov ebx, 1
        mov ecx, [ebp + 8]
        mov edx, 10
        int 80h

        pop ebp
        ret


AddProc:
        mov edx, eax
        add edx, ebx
        add edx, ecx
        mov eax, edx
        ret
