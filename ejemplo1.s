

.text
.globl fact
.type fact, @function

fact:
	# PROLOGO 
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $(1), %eax
	movl %eax, -4(%ebp)

start1:
	movl 8(%ebp), %eax
	pushl %eax
	movl $(1), %eax
	movl %eax, %ebx
	popl %eax
	cmpl %eax, %ebx
	jle greaterThan1
	movl $(1), %eax
	jmp fin_greaterThan1
greaterThan1:
	movl $(0), %eax
fin_greaterThan1:
	cmpl $0, %eax
	je final1
	
	movl -4(%ebp), %eax
	pushl %eax
	movl 8(%ebp), %eax
	movl %eax, %ebx
	popl %eax
	imull %ebx, %eax
	movl %eax, -4(%ebp)
	jmp start1

final1:
	movl 8(%ebp), %eax
	pushl %eax
	movl $(1), %eax
	movl %eax, %ebx
	popl %eax
	subl %ebx, %eax
	movl %eax, 8(%ebp)
	movl -4(%ebp), %eax

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

	subl $4, %esp
	movl $(6), %eax
	pushl %eax
	call fact
	addl $(8), %esp
	movl %eax, -4(%ebp)
	subl $4, %esp
	subl $4, %esp
	movl $(2), %eax
	movl %eax, -12(%ebp)
	subl $4, %esp
	movl $(0), %eax
	movl %eax, -16(%ebp)
	movl -12(%ebp), %eax
	pushl %eax
	movl -16(%ebp), %eax
	movl %eax, %ebx
	popl %eax
	addl %ebx, %eax
	pushl %eax
	movl $(6), %eax
	movl %eax, %ebx
	popl %eax
	imull %ebx, %eax
	pushl %eax
	movl $(3), %eax
	movl %eax, %ebx
	popl %eax
	cdq
	idivl %ebx
	movl %eax, -8(%ebp)
	movl $(1), %eax
	pushl -8(%ebp)
	movl %eax, %ebx
	popl %eax
	addl %ebx, %eax
	movl %eax, -8(%ebp)
	movl $(0), %eax

	# EPILOGO 
	movl %ebp, %esp
	popl %ebp
	ret