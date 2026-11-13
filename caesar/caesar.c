// Libraries to include
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function declarations
bool only_digit(string s);
int rotate(char c, int i);

//---
int main(int argc, string argv[]) {
    // Variables
    int key = 0;
    string text;

    if (argc >= 3 || argc <= 1) {
        printf("Please use one command line argument.\n");
        return 1;
    }

    if (only_digit(argv[1]) == false) {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    key = atoi(argv[1]);

    text = get_string("Plaintext: ");

    for (int i = 0, n = strlen(text); i < n; i ++) {
        text[i] = rotate(text[i], key);
    }

    printf("ciphertext: %s\n", text);
}

//---
bool only_digit(string s) {
    for (int i = 0, n = strlen(s); i < n; i++) {
        if (isdigit(s[i]) == 0) {
            return false;
        }
    }
    return true;
}

//---
int rotate(char c, int i) {
    if (isalpha(c)){
        int t;
        if (isupper(c)) {
            t = c - 65;
        } else if (islower(c)) {
            t = c - 97;
        }

        for (int j = 0; i > j; i--) {
            t++;
            if (t >= 26){
                t = 0;
            }
        }

        if (isupper(c)) {
            t = t + 65;
        } else if (islower(c)) {
            t = t + 97;
        }

        return t;
    } else {
        return c;
    }
}
