// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 52;

// Hash table
node *table[N];

// Define counter
int count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Find the index of the word being checked
    int index = hash(word);

    // Access the location in the hash table
    if (table[index] != NULL)
    {
        // Set up the cursor
        node *cursor = table[index];

        // While cursor is pointing to a word
        while (cursor != NULL)
        {
            if (strcasecmp(cursor->word, word) == 0)
            {
                // If cursor word is == the word we are looking for, return true
                return true;
            }
            // If not, then move to the next word in the list
            cursor = cursor->next;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{

    // Original: return toupper(word[0]) - 'A';  <--- First letter of word

    int a = toupper(word[0]) - 'A'; // Get first letter value
    int b = toupper(word[1]) - 'A'; // Get second letter value

    // Make sure word is always a non-negative
    if (a < 0)
    {
        a = 0;
    }
    else if (b < 0)
    {
        b = 0;
    }

    // Return the two added together
    return a + b;

}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }

    char word[LENGTH+1];

    // Create a new node for each word
    while (fscanf(source, "%s", word) != EOF)
    {
        count ++;

        // Allocate memory for a new node
        node *newNode = malloc(sizeof(node));
        if (newNode == NULL)
        {
            return false;
        }

        // Copy new word into the node
        strcpy(newNode->word, word);
        // Set the next pointer
        newNode->next = NULL;

        // Get the index of a word by calling the hash function
        int index = hash(word);

        // If there is nothing in the hash table at the index location
        if (table[index] == NULL)
        {
            // Add in the new node
            table[index] = newNode;
        }
        // If there is something in the hash table at the index location
        else
        {
            // Set the "next" pointer of newNode to the current head
            newNode->next = table[index];
            //then add in the new node
            table[index] = newNode;
        }
    }
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO

    // For every index item in the table
    for (int i = 0; i < N; i++)
    {
        // Create a temp and cursor value
        node *cursor = table[i];
        node *temp = table[i];
        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(temp);
            temp = cursor;
        }
    }

    return true;
}
