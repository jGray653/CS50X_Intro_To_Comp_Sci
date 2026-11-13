from cs50 import get_float

while True:
    dollars = get_float("Change: ")
    # Check that dollars is non-negative
    if dollars > 0:
        break

# Initialize coins
quarters = 0
dimes = 0
nickels = 0
pennies = 0

# How many Quarters?
while dollars >= 0.25:
    dollars = round(dollars - 0.25, 2)
    quarters += 1

# How many Dimes?
while dollars >= 0.10:
    dollars = round(dollars - 0.10, 2)
    dimes += 1

# How many Nickels?
while dollars >= 0.05:
    dollars = round(dollars - 0.05, 2)
    nickels += 1

# How many Pennies?
while dollars >= 0.01:
    dollars = round(dollars - 0.01, 2)
    pennies += 1

print(quarters)
print(dimes)
print(nickels)
print(pennies)

coins = quarters + dimes + nickels + pennies

print(coins)
