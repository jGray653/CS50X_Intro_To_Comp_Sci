#include <stdio.h>
#include <cs50.h>

int main(void) {
    while (true) {
        int height = get_int("Height: ");

        if (height > 8 || height < 1) {
            continue;
        }
        else {
            for (int h = 0; h < height; h++) {
                for (int s = (height - 2); s >= h; s--) {
                    printf(" ");
                }
                for (int i = 0; i <= h; i++) {
                    printf("#");
                }
                printf("  ");
                for (int j = 0; j <= h; j++) {
                    printf("#");
                }
                printf("\n");
            }
            break;
        }
    }
}
