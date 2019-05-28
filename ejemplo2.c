int fact(int n) {
    int acum;
    acum = 1;
    while (n > 1) {
        acum = acum * n;
    }
    n = n - 1;
    return acum;
}

int numero;

int main() {
    
    printf("Dame un entero : ");
    scanf("%d", &numero);
    printf("El factorial = %d\n", fact(numero)); 
    
    return 0;
}
 