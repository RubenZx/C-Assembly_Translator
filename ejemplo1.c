
int fact(int n)
{
    if (n <= 1){
        return 1;
    }
    else{
        return n * fact(n-1);
    }
}

int numb;

int main()
{
    printf("Enter a number: ");
    scanf("%d", &numb);
    printf("Factorial = %d\n", fact(numb));
    
    return 0;
} 