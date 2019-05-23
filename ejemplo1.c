
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
    
    int factorial_6 = fact(6);

    return 0;
}
