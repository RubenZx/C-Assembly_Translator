int fact(int n)
{
    int aux = 0;
    if (n <= 1){
        aux = 1;
    }else{
        aux = n * fact(n-1);
    }
    return aux;
}

int numero;

int main() {

    printf("Dame un entero : ");
    scanf("%d", &numero);
    printf("El factorial = %d\n", fact(numero));
    return 0;
}