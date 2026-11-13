#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int score(string word);

int main(void) {
    string play1 = get_string("Player 1: ");
    string play2 = get_string("Player 2: ");

    int score1 = score(play1);
    int score2 = score(play2);

    if (score1 > score2) {
        printf("Player 1 Wins!\n");
    } else if (score1 < score2) {
        printf("Player 2 Wins!\n");
    } else {
        printf("Tie!\n");
    }
}

int score(string word) {
    int score = 0;

    for (int i = 0, len = strlen(word); i < len; i++) {
        if (isupper(word[i])) {
            score += points[word[i] - 'A'];
        }
        else if (islower(word[i])) {
            score += points[word[i] - 'a'];
        }
    }
    return score;
}
