#!/usr/bin/python3
print("how many cats do you have?")
numCats = input()
try:
    if int(numCats) >=4:
        print("That is alot of cats.")
    else:
        print("that is not that many cats.")
except ValueError:
    print("You did not enter a number.")

