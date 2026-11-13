#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BUFFER 512
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // files generated shouold be named ###.jpg, where ### is a 3 digit number
    // starting with 000 and working up
    // must not leak memory if using malloc


    // Accept one single-line argument only
    if (argc != 2)
    {
        printf("Useage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Card not found\n");
        return 1;
    }

    // Create a buffer for the blocck of data
    BYTE buffer[BUFFER];
    //See how to improve this
    int count = 0;
    int foundcount = 0;
    FILE *img = NULL;

    // While still data left to read from the memory card
    while (fread(buffer, 1, BUFFER, card) == BUFFER) // When fread reaches 0, loop stops
    {
        // Checking that is a new jpg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //check if first jpg
            if (foundcount == 0)
            {
                foundcount = 1;
            }
            else
            {
                fclose(img);
            }
            char filename[8];
            sprintf(filename, "%03i.jpg", count);
            img = fopen(filename, "a");
            count += 1;
        }
        if (foundcount == 1)
        {

            fwrite(&buffer, 1, BUFFER, img);
        }
    }
    fclose(img);
    fclose(card);
}
