import csv
import sys


def main():

    # Check for command-line usage
    # If the command line doesn't have exactly 3 arguments
    if len(sys.argv) != 3:
        # Print Error Message
        print("Usage: python dna.py databases/___.csv sequences/___.txt")

    # Read database file into a variable
    database = []
    dnas = []

    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        dnas = reader.fieldnames

        for row in reader:
            i = 0
            # Initialise a new dictionary for a new person
            person = {}
            while i < len(dnas):
                # Add to the dictionary for each trait
                person.update({dnas[i]: row[dnas[i]]})
                i += 1
            # Add the person to the list
            database.append(person)

    # Make the list of headings usible through the rest of the code.
    dnas.remove("name")

    # Read DNA sequence file into a variable
    with open(sys.argv[2]) as file:
        for line in file:
            sequ = line

    # TODO: Find longest match of each STR in DNA sequence
    matches = {}
    i = 0

    while i < len(dnas):
        # Find the longest match for each string
        num = longest_match(sequ, dnas[i])
        # Add to a dictionary of the longest matches
        matches[dnas[i]] = num
        i += 1

    # Check database for matching profiles
    i = 0
    j = 0
    person = "No Match"

    while j < len(database):
        while i < len(dnas):

            if (int(database[j][dnas[i]]) == matches[dnas[i]]):
                person = database[j]["name"]
                i += 1
            else:
                person = "No Match"
                i = 0
                break
        j += 1

    print(person)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


main()
