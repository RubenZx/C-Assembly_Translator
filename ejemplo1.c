int x;

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
    int a, b = 2, c = 0;

    a = (b + c) * 6 / 3;
    a += 1;
    
    return 0;
}
