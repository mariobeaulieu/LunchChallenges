#!/usr/bin/python3
import sys

dbg=False
maxNum = 0
maxGrd = 0
numbers = [[], [], [], [], [], [], [], [], [], [], [], [], []]
grid =    ["", "", "", "", "", "", "", "", "", "", "", "", ""]
def read_grid(filename: "Numbers.txt"):
    global numbers, grid, maxNum, maxGrd
    reading_numbers = True
    gridline = 0
    file = open(filename, "r")
    line = file.readline().strip()
    length = len(line)
    while length > 0:
        if reading_numbers:
            if line != "GRID":
                if dbg: print(f"{length}-digit number: <{line}>")
                numbers[length].append(line)
                if length>maxNum:
                    maxNum=length
                    if dbg: print(f"Maximum length of numbers set to {maxNum}")
            else:
                reading_numbers = False
        else:
            if dbg: print(f"Grid: <{line}>")
            for i in range(length):
                if line[i] == "0":
                    grid[maxGrd]+="⬜"
                else:
                    grid[maxGrd]+="🟥"
            maxGrd += 1
        line = file.readline().strip()
        length = len(line)

def print_grid():
    global grid, maxGrd
    print ("\n\nGRID:")
    for i in range(maxGrd):
        print (grid[i])

def print_numbers():
    global numbers, maxNum
    print ("\n\nNUMBERS:")
    for i in range(3,maxNum+1):
        if dbg: print(f"There are {len(numbers[i])} {i}-character numbers)")
        if len(numbers[i]) != 0:
            print(f"{i}: {numbers[i]}")

read_grid("Numbers.txt")
# print("Numbers")
# print(numbers)
# print("Grid")
# print(grid)

print_grid()
print_numbers()

