from cs50 import get_int

# Until the loop breaks
while True:
    # Ask user for a height
    height = get_int("Pyramid Height 1-8: ")
    # Check if height is within a given range
    if height < 1 or height > 8:
        # If not then prompt again
        print("Height must be between 1 and 8 inclusive")
    else:
        # If it is then breaks the loop
        break

# For each row in the given height
for i in range(height):
    # Find whitespace of the triangle row
    s = height - i - 1
    for _ in range(s):
        print(" ", end='')
    for j in range(i + 1):
        print("#", end='')
    # Print the two empty spaces in the middle
    print("  ", end='')
    # Other half of triangle
    for h in range(i + 1):
        print("#", end='')
    print()
