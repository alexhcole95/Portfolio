# -- Calculator to Specify How Much Sugar and Water is Needed for Syrup -- #

## IMPORTS ##
import numpy as np

## FUNCTIONS ##
def instructions():
    # FUNCTION TO GIVE INSTRUCTIONS ON PROGRAM
    print()
    print()
    print('This calculator allows you to select either 1:1 or 2:1 syrup depending on your needs.')
    print('Once the ratio has been selected, you will be prompted to select your syrup amount (in gallons).')
    print('At this point, the program runs, and you will receive an output that declares the exact amount of sugar and water (in quarts) needed for the desired syrup.')
    print('For 1:1 syrup, each .1gal of syrup uses .24qt/water and .29qt/sugar.')
    print('For 2:1 syrup, each .1gal of syrup uses .16qt/water and .42qt/sugar.')
    print()

def spring():
    # FUNCTION FOR SPRING SYRUP CONSISTENCY
    spring_syrup = (input("\nHow many gallons of spring syrup would you like?\t"))

    total_water = 0.0
    total_sugar = 0.0
    for _ in np.arange(0, float(spring_syrup), 0.1):
        total_water += 0.24
        total_sugar += 0.29
    print("You'll need " + format(total_water, '.2g') + "qts of water and " + format(total_sugar, '.2g') + "qts of sugar to make " + spring_syrup + " gallon(s) of spring syrup.")

def fall():
    # FUNCTION FOR FALL SYRUP CONSISTENCY
    fall_syrup = (input("\nHow many gallons of fall syrup would you like?\t"))
    total_water = 0.0
    total_sugar = 0.0

    for _ in np.arange(0, float(fall_syrup), 0.1):
        total_water += 0.16
        total_sugar += 0.42

    print("You'll need " + format(total_water, '.2g') + "qts of water and " + format(total_sugar, '.2g') + "qts of sugar to make " + fall_syrup + " gallon(s) of fall syrup.")

## LOGIC ##
print("----> Welcome to Alex Cole's Syrup Calculator for Honey Bees! <----")

# WHILE LOOP FOR SYRUP CALCULATOR
while True:
    value = (input('\nWould you like spring (1:1) syrup or fall (2:1) syrup? If needed, type in "help" and press Enter for instructions.\t'))

    if value == 'help' or value == 'Help':
        instructions()
        continue

    elif value == '1:1' or value == 'spring':
        spring()
        break

    elif value == '2:1' or value == 'fall':
        fall()
        break

    else:
        print('INVALID. TRY AGAIN.')
        continue
