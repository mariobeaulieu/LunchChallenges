#include <stdio.h>
#define SIZE 5

/*
00 01 02 03
10 11 12 13
20 21 22 23
30 31 32 33
 */

int main() {
    int a[SIZE][SIZE];
    int i,j, x = 0, k;
    for(i = 0; i < SIZE; i++) {
        for (j = 0; j < SIZE; j++) {
            a[i][j] = x++;
        }
    }

    for (k = 0; k < (SIZE+1)/2 ; k++) {
        for(i = k; i < SIZE-k; i++) {
            printf("%d,%d ", i, k);
        }
        if (k<SIZE-k) printf("\n");
        for(i = k+1; i < SIZE-k; i++) {
            printf("%d,%d ", SIZE-k-1, i);
        }
        if (k+1<SIZE-k) printf("\n");
        for(i = k+1; i < SIZE-k; i++) {
            printf("%d,%d ", SIZE-1-i, SIZE-k-1);
        }
        if (k+1<SIZE-k) printf("\n");
        for(i = k+1; i < SIZE-k-1; i++) {
            printf("%d,%d ", k, SIZE-1-i);
        }
        if (k+1<SIZE-k-1) printf("\n");
    }
}

