int main() {
    int sum = 0;
    int i = 0;
    while (i < 10) {
        sum = sum + i;
        i = i + 1;
    }
    
    int j;
    for (j = 0; j < 5; j = j + 1) {
        sum = sum + j;
    }
    
    if (0) {
        sum = 0;
    }
    
    return sum;
}
