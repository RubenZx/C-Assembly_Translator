.text
.globl main
.type main, @function

main:
	pushl %ebp
	movl %esp, %ebp
	subl $4, %esp
	movl $(1), %eax
	movl %eax,-4(%ebp)
	movl -4(%ebp), %eax
	pushl %eax;
	movl $(2), %eax
	pushl %eax;
	movl -4(%ebp), %eax
	movl %eax, %ebx;
	popl %eax;
	imull %ebx, %eax;
	movl %eax, %ebx;
	popl %eax;
	addl %ebx, %eax;
	movl %eax,-4(%ebp)
	subl $4, %esp
	movl $(0), %eax
	movl %ebp, %esp
	popl %ebp
	ret