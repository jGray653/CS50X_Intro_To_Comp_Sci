// Libraries to Include
#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Function Initialisation
int count_let(string text);
int count_wor(string text);
int count_sen(string text);

// Main Function
int main(void) {
    // Prompt user for some text:
    string input = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text
    // needs to create and assign the L and S variables
    float letters = count_let(input);
    float words = count_wor(input);
    int sentence = count_sen(input);

    // Compute the Coleman-Liau index
    // index = 0.0588 * L - 0.296 * S - 15.8;
    // L is the average number of letters per 100 words of text.
    //   that is, the number of letters divided by the number of words, all multiplied by 100.
    float L = letters / words * 100;
    // S is the average amount of sentences per 100 words.
    //  that is, the number of sentences divided by the number of words, all multiplied by 100.
    float S = sentence / words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index < 1) {
        printf("Before Grade 1\n");
    } else if (index > 16){
        printf("Grade 16+\n");
    }
    else {
        printf("Grade %i\n", index);
    }
}

// Count Letters
int count_let(string text) {
    int count = 0;

    for (int i = 0, n = strlen(text); i < n; i++) {
        if (isalpha(text[i])) {
            count++;
        }
    }

    return count;
}

// Count Words
int count_wor(string text) {
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++) {
        if (isspace(text[i])) {
            count++;
        }
    }
    count++;

    return count;
}

// Count Sentences
int count_sen(string text) {
    int count = 0;

    for (int i = 0, n = strlen(text); i < n; i++) {
        if (text[i] == 46) {
            count++;
        } else if (text[i] == 33) {
            count++;
        } else if (text[i] == 63) {
            count++;
        }
    }
    return count;
}
