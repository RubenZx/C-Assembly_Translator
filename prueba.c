
int main()
{
    int a = 1;
    a = a + 2 * a;
    
    int b;

    return 0;
}

// _________________________
// -------int main():-------
// -------------------------
// .text 
// .globl main
// .type main, @function
// main:
//  pushl %ebp
//  movl %esp, %ebp
// _________________________
// -------(int a) = 1;------
// -------------------------
//  subl $4, %esp
//  movl $1, -4(%ebp) 
//  # restamos 4 a la pila
// _________________________
// -------int a (= 1;)------
// -------------------------
//  movl $1, -4(%ebp)
//  movl -4(%ebp), %eax
//  # pasamos 'a' a eax usando tabla
//  pushl %eax
//  # y lo metemos en la pila
// _________________________
// --------a=a+(2*a);-------
// -------------------------
//  movl $2, %eax
//  pushl %eax
//  # metemos el 2 en la pila
//  movl -4(%ebp), %eax
//  # metemos 'a' en eax
//  movl %eax, %ebx
//  popl %eax
//  imull %ebx, %eax 
//  # en %eax: 2*a
// -------------------------
// --------a=(a+%eax)-------
// -------------------------
//  movl %eax, %ebx
//  popl %eax
//  addl %ebx, %eax
//  # en %eax: a+2*a
// -------------------------
// --------(a=a+%eax)-------
// -------------------------
//  movl %eax, -4(%ebp) 
// -------------------------
// ----------int b;---------
// -------------------------
//  subl $4(%esp)
// -------------------------
// ---------return 0;-------
// -------------------------
//  addl $8, %esp # quitar params
//  # 8 por los 2 params
//  movl $0, $eax
//  # return 0
// -------------------------
// ---------EPILOGO---------
// -------------------------
//  movl %ebp, %esp
//  popl %ebp
//  ret
