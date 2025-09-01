#!/usr/bin/python3
import sys
import tkinter as tk

dbg=True
maxNum = 0
maxGrd = 0
validFile=False
numbers = [[], [], [], [], [], [], [], [], [], [], [], [], []]
taken = [[], [], [], [], [], [], [], [], [], [], [], [], []]
grid =    ["", "", "", "", "", "", "", "", "", "", "", "", ""]

def read_grid(filename: "Numbers.txt"):
    global numbers, grid, maxNum, maxGrd, validFile
    reading_numbers = True
    numDigits=0
    numCases=0
    gridline = 0
    file = open(filename, "r")
    line = file.readline().strip()
    length = len(line)
    while length > 0:
        if reading_numbers:
            if line != "GRID":
                if dbg: print(f"{length}-digit number: <{line}>")
                numbers[length].append(line)
                taken[length].append(False)
                numDigits+=length
                if length>maxNum:
                    maxNum=length
                    if dbg: print(f"Maximum length of numbers set to {maxNum}")
            else:
                reading_numbers = False
        else:
            if dbg: print(f"Grid: <{line}>")
            for i in range(length):
                if line[i] == "0":
                    grid[maxGrd]+=" "
                    numCases+=1
                else:
                    grid[maxGrd]+="#"
            maxGrd += 1
        line = file.readline().strip()
        length = len(line)
    if numCases*2 != numDigits:
        print (f"Error in the file: {numDigits} digits should be an even number and should be equal to 2* number of cases (={numCases})")
    else:
        validFile = True
        print(f"\nFile OK: {numDigits} digits fit correctly in {numCases} cases: 2*{numCases}={numDigits}")

def print_grid():
    global grid, maxGrd
    root = tk.Tk()
    root.title("Fill Numbers Game")
    root.geometry("500x500")

    for i in range(maxGrd):
        for j in range(maxGrd):
            if grid[i][j] != "#":
                fgcol = "black"
                bgcol = "white"
                tx = grid[i][j]
            else:
                fgcol = "white"
                bgcol = "black"
                tx = " "
            tk.Button(root, text=tx, fg=fgcol, bg=bgcol).grid(row=i, column=j, padx=0, pady=0)
    root.mainloop()

def print_numbers():
    global numbers, maxNum
    print ("\n======== NUMBERS =========")
    for i in range(3,maxNum+1):
        if dbg: print(f"There are {len(numbers[i])} {i}-character numbers)")
        if len(numbers[i]) != 0:
            print(f"{i}: {numbers[i]}")

class Start_cell:
    def __init__(self, row, col, horizontal):
        self.row = row
        self.col = col
        # horizontal is TRUE if the position refers to a horizontal start position. False if it's vertical
        # The same cell can have 2 entries, one for vertical and one for horizontal
        self.horizontal = horizontal

class Cell:
    # A cell contains a digit for a horizontal number and for a vertical number.
    # Upon creation, the position within the horizontal number is known (0=start of the number)
    # as well as the length of that number
    # The length and position in vertical number will be set later
    # Values -1 mean not set yet
    # Black squares in the grid are with contains_number=False
    def __init__(self, contains_number=False, hor_pos=-1, hor_num_length=-1):
        self.contains_number = contains_number
        self.hor_pos = hor_pos
        self.ver_pos = -1
        self.value = -1
        self.hor_num_length = hor_num_length
        self.ver_num_length = -1
        self.num_known_h = 0
        self.num_known_v = 0
    def set_hor_pos(self, h):
        self.hor_pos = h
        self.contains_number = True
    def set_ver_pos(self, v):
        self.ver_pos = v
        self.contains_number = True
    def set_hor_num_length(self, l):
        self.hor_num_length = l
    def set_ver_num_length(self, l):
        self.ver_num_length = l


class Game:
    def __init__(self, num_list, size, grid, dbg):
        # xy is an array of up to 13 lines and columns and each entry contains a Cell
        self.xy = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        self.start_positions = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        self.num_list = num_list.copy()
        self.grid = grid
        # Initialize the whole grid as an array of black cells
        for i in range(size):
            for j in range(size):
                self.xy[i].append(Cell())
        # Use the grid to change black cells into number cells and set the horizontal pos in the number
        if dbg: print(f"Creating the Game grid with size {size} x {size}")
        for i in range(size):
            h=0
            for j in range(size):
                if grid[i][j] != "#":
                    # if dbg: print(f"grid[{i},{j}] is horizontal position {h} in number")
                    self.xy[i][j].set_hor_pos(h)
                    h+=1
                else:
                    h=0
        for j in range(size):
            v=0
            for i in range(size):
               if grid[i][j] != "#":
                   # if dbg: print(f"grid[{i},{j}] is vertical position {v} in number")
                   self.xy[i][j].set_ver_pos(v)
                   v += 1
               else:
                   v = 0
        # Set number length horizontally
        for i in range(size):
            h=0
            for j in range(size-1,-1,-1):
                if self.xy[i][j].contains_number:
                    if h == 0: h = self.xy[i][j].hor_pos+1
                    self.xy[i][j].set_hor_num_length(h)
                else:
                    h=0
        # Set number length vertically
        for j in range(size):
            v=0
            for i in range(size-1,-1,-1):
                if self.xy[i][j].contains_number:
                    if v == 0: v = self.xy[i][j].ver_pos+1
                    self.xy[i][j].set_ver_num_length(v)
                else:
                    v=0

    def set_cell_value(self, i, j, v):
        # When setting a cell value, it also increments the number of known letters of vertical and horizontal numbers
        c = self.xy[i][j]
        if dbg:
            print(f"Setting cell [{i},{j}] to value {v}")
        # the value is already set, nothing to do
        if c.value == v: return True
        c.value = v

        self.grid[i] = self.grid[i][0:j]+v+self.grid[i][j+1:]
        lh = c.hor_num_length
        lv = c.ver_num_length
        if dbg: print(f"Writing {v} at {i},{j}, hor len is {lh}, ver len is {lv}")
        self.xy[i][j-c.hor_pos].num_known_h += 1
        # If all digits on horizontal number are known, remove that entry from num_list
        if self.xy[i][j-c.hor_pos].num_known_h == lh:
            value = ""
            for n in range(lh):
                vv=self.xy[i][j-c.hor_pos+n].value
                value += vv
            self.num_list[lh].pop(self.num_list[lh].index(value))
            if dbg: print(f"Removed entry {value}: that entry was used horizontally")
        # If all digits on vertical number are known, remove that entry from num_list
        self.xy[i-c.ver_pos][j].num_known_v += 1
        if self.xy[i-c.ver_pos][j].num_known_v == lv:
            value = ""
            for n in range(lv):
                vv = self.xy[i-c.ver_pos+n][j].value
                print(f"[{i},{j}]: c.ver_pos={c.ver_pos}, n={n}, value={value}, vv={vv}")
                value += vv
            self.num_list[lv].pop(self.num_list[lv].index(value))
            if dbg: print(f"Removed entry {value}: that entry was used vertically")

    # Write a number horizontally, return False if conflict
    def check_write_horizontal(self, i, j, value):
        ll = len(value)
        if dbg: print(f"Writing {value} to line {i} pos {j}], hor_pos={self.xy[i][j].hor_pos}, len={self.xy[i][j].hor_num_length}")
        if self.xy[i][j].hor_pos != 0: return False
        if ll != self.xy[i][j].hor_num_length: return False
        for n in range(ll):
            cell=self.xy[i][j+n]
            if dbg: print(f"Cell value is {cell.value}, compared to {value[n]}")
            if cell.value != value[n] and cell.value != -1: return False
        return True

    def write_horizontal(self, i, j, value):
        for n in range(len(value)):
            self.set_cell_value(i, j+n, value[n])

    # Write a number vertically, return False if conflict
    def check_write_vertical(self, i, j, value):
        ll = len(value)
        if dbg: print(f"Writing {value} to column {j} pos {i}], ver_pos={self.xy[i][j].ver_pos}, len={self.xy[i][j].ver_num_length}")
        if self.xy[i][j].ver_pos != 0: return False
        if ll != self.xy[i][j].ver_num_length: return False
        for n in range(ll):
            cell=self.xy[i+n][j]
            if dbg: print(f"Cell value is {cell.value}, compared to {value[n]}, ll={ll}")
            if cell.value != value[n] and cell.value != -1: return False
        return True

    def write_vertical(self, i, j, value):
        for n in range(len(value)):
            self.set_cell_value(i+n, j, value[n])

    # Generate the list of start positions of numbers in the grid
    def get_start_positions(self):
        # Reset the list of start positions
        g.start_positions = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        for i in range(0, maxGrd):
            for j in range(0, maxGrd):
                ll = self.xy[i][j].hor_num_length
                if self.xy[i][j].hor_pos == 0 and self.xy[i][j].num_known_h < ll:
                    g.start_positions[ll].append(Start_cell(i,j,True))
                ll = self.xy[i][j].ver_num_length
                if self.xy[i][j].ver_pos == 0 and self.xy[i][j].num_known_v < ll:
                    g.start_positions[ll].append(Start_cell(i,j,False))
        if dbg:
            for i in range(0, maxGrd):
                nb = len(g.start_positions[i])
                if nb>0:
                    print(f"Start cells for {i} char numbers are:")
                    for j in range(0, nb):
                        if g.start_positions[i][j].horizontal:
                            dir="horizontal"
                        else:
                            dir="vertical"
                        print(f"[{g.start_positions[i][j].row},{g.start_positions[i][j].col}]->{dir}")


def debug_data():
    global g
    for i in range(0,4):
        for j in range(0,4):
            print(f"[{i},{j}]: HorPos={g.xy[i][j].hor_pos}, VerPos={g.xy[i][j].ver_pos}, Value={g.xy[i][j].value}")

read_grid("Numbers.txt")

if validFile:
    g=Game(numbers, maxGrd, grid, dbg)
    print_grid()
    g.get_start_positions()
    n=numbers[9][1]
    i=10
    j=4
    if g.check_write_horizontal(i,j,n):
        g.write_horizontal(i,j,n)
        print_grid()
    else:
        print(f"Couldn't write horizontally at position [{i},{j}] the number {n}")

    n=numbers[3][10]
    i=0
    j=2
    if g.check_write_vertical(i,j,n):
        g.write_vertical(i,j,n)
        print_grid()
    else:
        print(f"Couldn't write vertically at position [{i},{j}] the number {n}")

    n=numbers[3][4]
    i=0
    j=1
    if g.check_write_vertical(i,j,n):
        g.write_vertical(i,j,n)
        print_grid()
    else:
        print(f"Couldn't write vertically at position [{i},{j}] the number {n}")

    n=numbers[3][1]
    i=0
    j=0
    if g.check_write_vertical(i,j,n):
        g.write_vertical(i,j,n)
        print_grid()
    else:
        print(f"Couldn't write vertically at position [{i},{j}] the number {n}")

    print_numbers()
