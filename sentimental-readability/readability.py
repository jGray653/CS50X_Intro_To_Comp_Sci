from cs50 import get_string

def main():
    # Prompt user for a text string
    input = get_string("Text: ")

    # Count Letters, words, and sentences
    letters = count_let(input)
    words = count_wor(input)
    sentences = count_sen(input)

    # Compute the Coleman-Liau Index
    # index = 0.0588 * L - 296 * S - 15.8
    # L = average no of letters per 100 words
    L = letters / words * 100

    # S = average sentences per 100 words
    S = sentences / words * 100

    index = round(0.0588 * L - 0.296 * S - 15.8)

    if index < 1 :
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


# Count Letters
def count_let(s):
    count = 0

    for l in s:
        if l.isalpha():
            count += 1

    return count

# Count Words
def count_wor(s):
    count = 0

    for l in s:
        if l.isspace():
            count += 1
    count += 1

    return count

# Count Sentences
def count_sen(s):
    count = 0

    for l in s:
        if l == ".":
            count += 1
        elif l == "!":
            count += 1
        elif l == "?":
            count += 1

    return count

main()
