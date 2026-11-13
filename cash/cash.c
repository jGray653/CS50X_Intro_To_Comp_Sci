#include <cs50.h>
#include <stdio.h>



int main(void) {
    int cents = 0;
    int quarters = 0;
    int dimes = 0;
    int nickels = 0;
    int pennies = 0;

    do {
        cents = get_int("Change Owed: ");
    } while (cents < 0);
    // how many quarters?
    while (cents >= 25) {
        cents = cents - 25;
        quarters++;
    }

    // how many dimes?
    while (cents >= 10) {
        cents = cents - 10;
        dimes++;
    }
    // how many nickels?
    while (cents >= 5) {
        cents = cents - 5;
        nickels++;
    }
    // how many pennies?
    while (cents >= 1) {
        cents = cents - 1;
        pennies++;
    }
    // sum of those?
    int coins = quarters + dimes + nickels + pennies;
    // print sum
    printf("%i\n", coins);
}
