

.text
.globl main
.type main, @function

main:
	pushl %ebp
	movl %esp, %ebp
	subl $4, %esp
	movl $(0), %eax
	movl %eax, -4(%ebp)
	movl $(1), %eax
	pushl -4(%ebp)
	movl %eax, %ebx
	popl %eax
	imull %ebx, %eax
	movl %eax, -4(%ebp)
	movl $(0), %eax
	movl %ebp, %esp
	popl %ebp
	ret