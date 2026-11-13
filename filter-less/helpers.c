#include "helpers.h"
#include <math.h>

void swap(int *a, int *b);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all of the pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take the average of RGB to convert to greyscale
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            int grey = round((red + green + blue) / 3.0);

            // Update pixel values
            image[i][j].rgbtRed = grey;
            image[i][j].rgbtGreen = grey;
            image[i][j].rgbtBlue = grey;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            // Update pixel with sepia values
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //Loop over all of the pixels vertically
    for (int i = 0; i < height; i++)
    {
        // loop over all of the pixels horizontally
        for (int j = 0, w = (width - 1); j < w; j++, w--)
        {
            //take fist pixel in row and switch it with the last pixel in the same row
            int tmpr = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][w].rgbtRed;
            image[i][w].rgbtRed = tmpr;

            int tmpg = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][w].rgbtGreen;
            image[i][w].rgbtGreen = tmpg;

            int tmpb = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][w].rgbtBlue;
            image[i][w].rgbtBlue = tmpb;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // take the target square, and the eight squares around it
    // find the average of their rgb values
    // update the target quare to have the new value

    // create a copy of the original image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Blurring part
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Variables
            float pixels = 0.0;
            int blurRed =0;
            int blurGreen = 0;
            int blurBlue = 0;

            // going over the copy image. starts off at one less than i
            // only proceeds if y is less than the total height AND either less rhan or equal to i + 1
            for (int y = i - 1; y < height && y <= i + 1; y++)
            {
                // the same as above, but on the x axis instead
                for (int x = j - 1; x < width && x <= j + 1; x++)
                {
                    // Checks that x and y are both valid non-negative numbers
                    if (x >= 0 && y >= 0)
                    {
                        // add the values to the totals
                        blurRed += copy[y][x].rgbtRed;
                        blurGreen += copy[y][x].rgbtGreen;
                        blurBlue += copy[y][x].rgbtBlue;
                        // update total valid pixel count
                        pixels += 1;
                    }
                }
            }

            // modify numbers and add to original image.
            image[i][j].rgbtRed = round(blurRed / pixels);
            image[i][j].rgbtGreen = round(blurGreen / pixels);
            image[i][j].rgbtBlue = round(blurBlue / pixels);
        }
    }

    return;
}
