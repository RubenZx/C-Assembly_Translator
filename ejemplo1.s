.section .rodata
.LC0:
	.string "Dame un entero : "
.LC1:
	.string "%d"
.LC2:
	.string "El factorial = %d\n"

.text
.globl fact
.type fact, @function

fact:
	# PROLOGO 
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $(0), %eax
	movl %eax, -4(%ebp)
	movl 8(%ebp), %eax
	pushl %eax
	movl $(1), %eax
	movl %eax, %ebx
	popl %eax
	cmpl %eax, %ebx
	jle lessEqual1
	movl $(0), %eax
	jmp fin_lessEqual1

lessEqual1:
	movl $(1), %eax

fin_lessEqual1:
	cmpl $0, %eax
	je false1
	
	movl $(1), %eax
	jmp return1
	jmp final1

false1:
	movl 8(%ebp), %eax
	pushl %eax
	movl 8(%ebp), %eax
	pushl %eax
	movl $(1), %eax
	movl %eax, %ebx
	popl %eax
	subl %ebx, %eax
	movl %eax, %ebx
	pushl %ebx
	call fact
	addl $(8), %esp
	movl %eax, %ebx
	popl %eax
	imull %ebx, %eax
	jmp return1

final1:

return1:
	# EPILOGO 
	movl %ebp, %esp
	popl %ebp
	ret

.text
.globl main
.type main, @function

main:
	# PROLOGO 
	pushl %ebp
	movl %esp, %ebp

	pushl $s0		# $s0 = Dame un entero : 
	call printf
	addl $(4), %esp
	pushl $numero, %eax
	pushl $s1		# $s1 = %d
	call scanf
	addl $(8), %esp
	movl numero, %eax
	movl %eax, %ebx
	pushl %ebx
	call fact
	addl $(8), %esp
	movl %eax, %ebx
	pushl %ebx
	pushl $s2		# $s2 = El factorial = %d\n
	call printf
	addl $(8), %esp
	movl $(0), %eax
	jmp return2

return2:
	# EPILOGO 
	movl %ebp, %esp
	popl %ebp
	ret