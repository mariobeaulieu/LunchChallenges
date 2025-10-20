#!/usr/bin/python3
import os
import tkinter as tk
from random import random

dbg=True
maxNum = 0
count = 0
step_mode = True
number_of_solutions = 0
value = ""
grid = [[]]
grid_size=0
designed = False
numcol = 4


def print_grid(game, pause=False, solution=False):
    global count, step_mode, root, number_of_solutions, grid_size
    count += 1
    if pause or step_mode:
        root = tk.Tk()
        if solution:
            number_of_solutions += 1
            root.title("Solution #"+str(number_of_solutions)+" found after "+str(count)+" attempts")
            solve_text="Again"
        else:
            root.title("Fill Numbers Game - "+str(count))
            solve_text="Solve it"
        grid_width = grid_size*38
        padding = 0
        firstcol=0
        if grid_width < 400:
            # If grid is too narrow, the title doesn't display correctly
            grid_width = 400
            # padding is to add some room to the left to center the grid
            padding=0 #((10-grid_size)*19, 0)
            firstcol=4
        middle = (grid_size-2)//2
        span=2
        if grid_size % 2 == 1:
            span=3

        for i in range(1, firstcol):
            tk.Label(root, text="  ", font="courier").grid(row=0, column=i-1)
        for i in range(grid_size):
            # paddingvalue is not 0 only for the first column
            paddingvalue=padding
            for j in range(grid_size):
                tx = " "
                if game.grid[i][j].contains_number:
                    fgcol = "black"
                    bgcol = "white"
                    if game.grid[i][j].value != -1:
                        tx = game.grid[i][j].value
                else:
                    fgcol = "white"
                    bgcol = "black"
                tk.Button(root, text=tx, fg=fgcol, bg=bgcol).grid(row=i, column=j+firstcol, padx=paddingvalue, pady=0)
                paddingvalue = 0
        fgcol = "black"
        bgcol = "white"

        # Add the list of numbers to use at the bottom of the grid
        # Create a list of all numbers with headers for the length of following numbers
        long_list=[]
        for i in range(len(game.num_list)):
            if len(game.num_list[i]) > 0:
                long_list += [str(i)+"-digit numbers"] + game.num_list[i]
        # Is all numbers have been placed, then skip that part
        rowspan=0
        colspan=0
        if len(long_list) > 0:
            # Numbers are shown as 4 columns
            num_per_col = (len(long_list)+numcol-1)//numcol
            # Split the long_list in "numcol" columns
            cols = ["" for i in range(numcol)]
            for i in range(len(long_list)):
                cols[i//num_per_col] += long_list[i] + "\n"
            rowspan=num_per_col//2
            colspan=(grid_size+2*firstcol+numcol-1)//numcol
            for i in range(numcol):
                tk.Label(root, text=cols[i]).grid(row=grid_size+1, rowspan=rowspan, column=i*colspan, columnspan=colspan)
        grid_height = (grid_size+rowspan+2)*34
        root.geometry(str(grid_width)+"x"+str(grid_height))
        tk.Button(root, text="Step", fg=fgcol, bg=bgcol, command=step_program).grid(row=grid_size+rowspan+2, column=firstcol, columnspan=2, padx=padding, pady=0)
        tk.Button(root, text=solve_text, fg=fgcol, bg=bgcol, command=continue_to_solution).grid(row=grid_size+rowspan+2, column=middle+firstcol, columnspan=span, padx=0, pady=0)
        tk.Button(root, text="Exit", fg=fgcol, bg=bgcol, command=lambda: exit()).grid(row=grid_size+rowspan+2,column=grid_size+firstcol-2, columnspan=2, padx=0, pady=0)
        root.mainloop()

def get_file():
    grid_width = 400
    root = tk.Tk()
    root.title("Read a Fill-In file")
    root.geometry(str(grid_width) + "x" + str(grid_width))
    label = tk.Label(root, anchor="center", text="Select a file").place(relx=0.5, rely=0.25, anchor="center")
    filelist = [ i for i in os.listdir() if ".txt" in i ]
    filelist.sort()
    if dbg:
        print(filelist)
    current_value = tk.StringVar(root)
    current_value.set("Select a file")
    drop = tk.OptionMenu(root, current_value,*filelist)
    drop.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)
    tk.Button(root, text="OK", command=lambda: root.quit()).place(relx=0.2, rely=0.8, anchor="w")
    tk.Button(root, text="Exit", command=lambda: exit()).place(relx=0.8, rely=0.8, anchor="e")
    root.mainloop()
    root.destroy()
    filename = current_value.get()
    print("Filename is "+filename)
    g = Game()
    g.filename = filename
    g.read_grid(filename)
    g.set_hor_ver_pos_in_grid()
    return g

def get_number_list(game):
    long_list=[]
    for i in range(len(game.num_list)):
        if len(game.num_list[i]) > 0:
            long_list += [str(i)+"-digit numbers"] + game.num_list[i]
    if len(long_list) > 0:
        # Numbers are shown as 4 columns
        num_per_col = (len(long_list)+numcol-1)//numcol
        # Split the long_list in "numcol" columns
        cols = ["" for i in range(numcol)]
        for i in range(len(long_list)):
            cols[i//num_per_col] += long_list[i] + "\n"
    return cols

def interactive_play():
    def set_value(x, y, game, grid, labels_of_numbers):
        def setval(v, x, y, game, grid, labels_of_numbers):
            keypadroot.destroy()
            print(x, y, v)
            if v==-1:
                game.set_cell_value(x, y, v)
                text="   "
            else:
                game.set_cell_value(x, y, str(v))
                text=" "+str(v)+" "
            grid[x][y].configure(text=text)
            cols = get_number_list(game)
            for i in range(numcol):
                labels_of_numbers[i].configure(text=cols[i])
        keypadroot=tk.Tk()
        keypadroot.title("Click value")
        for i in range(1,10):
            tk.Button(keypadroot, text=str(i), command=lambda v=i: setval(v, x, y, game, grid, labels_of_numbers)).grid(row=(i-1)//3, column=(i-1)%3)
        tk.Button(keypadroot, text="0", command=lambda: setval(0, x, y, game, grid, labels_of_numbers)).grid(row=3, column=0)
        tk.Button(keypadroot, text="DEL", command=lambda: setval(-1, x, y, game, grid, labels_of_numbers)).grid(row=3, column=1, columnspan=2)
        keypadroot.mainloop()

        if game.grid[x][y] != "-1":
            bgcol = "black"
            fgcol = "white"
        else:
            fgcol = "black"
            bgcol = "white"
        grid[x][y].configure(fg=fgcol, bg=bgcol)

    ###########################################
    # This is the beginning of interactive_play
    ###########################################
    # First, get a problem to play from a file
    game = get_file()
    # Keep a copy of the original list of numbers
    list_of_numbers = copy_list_of_lists(game.num_list)
    # Then draw the screen as arrows of buttons that call back set_value defined above
    root = tk.Tk()
    root.title("Interactive Play")
    grid_size = len(game.grid)
    labels_of_numbers=[tk.Label(root) for i in range(numcol)]
    fgcol = "black"
    bgcol = "white"
    # Create the grid using buttons
    # Size of buttons is calculated to fit grid_width
    grid = [["" for i in range(grid_size)] for j in range(grid_size)]
    for row in range(grid_size):
        for col in range(grid_size):
            if game.grid[row][col].contains_number:
                fgcol = "black"
                bgcol = "white"
                text = "   "
            else:
                # fgcol = "white"
                bgcol = "black"
                text = "___"
            grid[row][col] = tk.Button(root, text=text, fg=fgcol, bg=bgcol, font=('Courier', 14))
            grid[row][col].grid(row=row, column=col)
            # Configure the callback for cells that contain values
            if game.grid[row][col].contains_number:
                grid[row][col].configure(command=lambda i=row, j=col: set_value(i, j, game, grid, labels_of_numbers))
        bgcol = "white"
        fgcol = "black"
    # Add labels containing the list of numbers to use at the bottom of the grid
    cols = get_number_list(game)
    rowspan=(len(cols[0])+1)//2
    colspan=grid_size//numcol
    if colspan < 2:
        colspan = 2
    for i in range(numcol):
        labels_of_numbers[i].configure(text=cols[i])
        labels_of_numbers[i].grid(row=grid_size+1, rowspan=rowspan, column=i*colspan, columnspan=colspan)
    root.mainloop()

def copy_list_of_lists(mylist):
    return [[mylist[i][j] for j in range(len(mylist[i]))] for i in range(len(mylist))]

def copy_array_of_objects(mylist):
    return [[mylist[i][j].copy() for j in range(len(mylist[i]))] for i in range(len(mylist))]

def save_grid(game):
    global root, value
    def get_textinput():
        global value
        value = textBox.get("1.0", "end-1c")
        root.quit()

    value = ""
    root.destroy()
    root = tk.Tk()
    root.geometry("300x200")
    root.title("Save problem")
    tk.Label(root, text="Enter a name for the problem you want to save").place(relx=0.5, rely=0.3, anchor="center")
    textBox = tk.Text(root, height=1, width=20)
    textBox.place(relx=0.5, rely=0.6, anchor="center")
    tk.Button(root, text="OK", command=lambda: get_textinput()).place(relx=0.1, rely=0.9, anchor="w")
    tk.Button(root, text="Cancel", command=lambda: root.quit()).place(relx=0.9, rely=0.9, anchor="e")
    root.mainloop()
    root.destroy()

    filename = value
    if filename[-4:] != ".txt": filename += ".txt"

    if dbg: print("Filename is <"+filename+">")
    if len(filename) > 0:
        with open(filename, mode="w") as f:
            # Save the grid first
            for row in range(grid_size):
                line=""
                for col in range(grid_size):
                    if game.grid[row][col].contains_number:
                        line += "0"
                    else:
                        line += "#"
                f.write(line+"\n")
            # Now the numbers
            for ll in range(grid_size+1):
                nb = len(game.num_list[ll])
                if nb > 0:
                    for i in range(nb):
                        f.write(game.num_list[ll][i]+"\n")
        root = tk.Tk()
        root.geometry("300x200")
        root.title("Save problem")
        tk.Label(root, text="File "+filename+" has been created").place(relx=0.5, rely=0.3, anchor="center")
        tk.Button(root, text="OK", command=lambda: root.quit()).place(relx=0.5, rely=0.6, anchor="center")
        root.mainloop()
        root.destroy()

def step_program():
    global step_mode, root
    step_mode = True
    root.quit()

def continue_to_solution():
    global step_mode
    step_mode = False
    root.quit()

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
    def copy(self):
        c2 = Cell()
        c2.contains_number = self.contains_number
        c2.hor_pos = self.hor_pos
        c2.ver_pos = self.ver_pos
        c2.value = self.value
        c2.hor_num_length = self.hor_num_length
        c2.ver_num_length = self.ver_num_length
        c2.num_known_h = self.num_known_h
        c2.num_known_v = self.num_known_v
        return c2


class Game:
    def __init__(self):
        # grid is an array of up to grid_size_max lines and columns and each entry contains a Cell
        global dbg, grid_size
        # Grid is up to grid_size x grid_size
        # It comprises grid_size lines, and each line is a list of cells
        self.filename = ""
        self.grid = []
        self.num_list = []
        # start_positions is the list of x-y coordinates where a horizontal or vertical number starts
        self.start_positions = []
        # start_pos_order is a list of lists [count, index]
        # where count is the number of entries in start_positions[index]
        # and is ordered with the lowest count first.
        # [2, 9] means start_positions[9] has 2 entries of 9 digits
        self.start_pos_order = []
        # Use the grid to change black cells into number cells and set the horizontal pos in the number
        if dbg: print("Creating the Game grid with size "+str(grid_size)+" x "+str(grid_size))

    def set_hor_ver_pos_in_grid(self):
        for row in range(grid_size):
            h=0
            for col in range(grid_size):
                if self.grid[row][col].contains_number:
                    self.grid[row][col].set_hor_pos(h)
                    h+=1
                else:
                    h=0
        for col in range(grid_size):
            v=0
            for row in range(grid_size):
                if self.grid[row][col].contains_number:
                   self.grid[row][col].set_ver_pos(v)
                   v += 1
                else:
                   v = 0
        # Set number length horizontally
        for row in range(grid_size):
            h=0
            for col in range(grid_size-1,-1,-1):
                if self.grid[row][col].contains_number:
                    if h == 0: h = self.grid[row][col].hor_pos+1
                    self.grid[row][col].set_hor_num_length(h)
                else:
                    h=0
        # Set number length vertically
        for col in range(grid_size):
            v=0
            for row in range(grid_size-1,-1,-1):
                if self.grid[row][col].contains_number:
                    if v == 0: v = self.grid[row][col].ver_pos+1
                    self.grid[row][col].set_ver_num_length(v)
                else:
                    v=0
        if dbg:
            for i in range(grid_size):
                for j in range(grid_size):
                    print("["+str(i)+":"+str(j)+"]: contains_number="+str(self.grid[i][j].contains_number)+", HorNumLen: "+str(self.grid[i][j].hor_num_length)+", HorPos: "+str(self.grid[i][j].hor_pos)+", VerNumLen: "+str(self.grid[i][j].ver_num_length)+", VerPos: "+str(self.grid[i][j].ver_pos))

    def copy(self):
        global grid_size
        newgame = Game()
        newgame.grid = copy_array_of_objects(self.grid)
        newgame.filename = self.filename
        newgame.num_list = copy_list_of_lists(self.num_list)
        newgame.start_positions = copy_list_of_lists(self.start_positions)
        newgame.start_pos_order = copy_list_of_lists(self.start_pos_order)
        return newgame

    def read_grid(self, filename) -> bool:
        global grid_size
        num_digits = 0
        num_cases = 0
        gridline = 0
        file = open(filename, "r")
        line = file.readline().strip()
        length = len(line)
        grid_size = length
        self.grid = [[Cell() for i in range(grid_size)] for j in range(grid_size)]
        self.num_list = [[] for i in range(grid_size+1)]
        while length > 0:
            # The grid is the first thing in the file
            # The grid is assumed to be square
            if gridline < grid_size:
                for i in range(length):
                    if line[i] == "0":
                        if dbg: print("[" + str(gridline) + "," + str(i) + "]: Contains_Number")
                        self.grid[gridline][i].contains_number = True
                        num_cases += 1
                    else:
                        if dbg: print("[" + str(gridline) + "," + str(i) + "]: Not a Number")
                        self.grid[gridline][i].contains_number = False
                gridline += 1
            else:
                if dbg: print(""+str(length)+"-digit number: <"+str(line)+">")
                self.num_list[length].append(line)
                num_digits += length
                if length > grid_size:
                    print("Number too long ("+str(length)+")\nMaximum length of numbers set to "+str(grid_size))
                    return False
            line = file.readline().strip()
            length = len(line)

        if num_cases * 2 != num_digits:
            print(
                f"Error in the file: "+str(num_digits)+" digits should be an even number and should be equal to 2* number of cases (="+str(num_cases)+")")
            return False
        else:
            print("\nFile OK: "+str(num_digits)+" digits fit correctly in "+str(num_cases)+" cases: 2*"+str(num_cases)+"="+str(num_digits))
            return True

    def create_grid(self, gg):
        # We have the grid as a list of rows of of "0" and "#"
        # We need to generate a "self.grid"
        self.grid = [[Cell() for i in range(grid_size)] for j in range(grid_size)]
        for row in range(grid_size):
            for col in range(grid_size):
                if gg[row][col] == "0":
                    self.grid[row][col].contains_number = True
                    self.grid[row][col].value = int(random()*10)
                else:
                    self.grid[row][col].contains_number = False

    def set_cell_value(self, i, j, v):
        # When setting a cell value, it also increments the number of known letters of vertical and horizontal numbers
        c = self.grid[i][j]
        if dbg:
            print("Setting cell ["+str(i)+","+str(j)+"] to value "+str(v))
        # the value is already set, nothing to do
        if c.value == v: return
        c.value = v

        # self.grid[i] = self.grid[i][0:j]+v+self.grid[i][j+1:]
        lh = c.hor_num_length
        lv = c.ver_num_length
        if dbg: print("Writing "+str(v)+" at "+str(i)+","+str(j)+", hor len is "+str(lh)+", ver len is "+str(lv))
        self.grid[i][j-c.hor_pos].num_known_h += 1
        # If all digits on horizontal number are known, remove that entry from num_list
        if self.grid[i][j-c.hor_pos].num_known_h == lh:
            value = ""
            for n in range(lh):
                vv=self.grid[i][j-c.hor_pos+n].value
                value += vv
            self.num_list[lh].pop(self.num_list[lh].index(value))
            if dbg: print("Removed entry "+str(value)+": that entry was used horizontally")
        # If all digits on vertical number are known, remove that entry from num_list
        self.grid[i-c.ver_pos][j].num_known_v += 1
        if self.grid[i-c.ver_pos][j].num_known_v == lv:
            value = ""
            for n in range(lv):
                vv = self.grid[i-c.ver_pos+n][j].value
                print("["+str(i)+","+str(j)+"]: c.ver_pos="+str(c.ver_pos)+", n="+str(n)+", value="+str(value)+", vv="+str(vv))
                value += vv
            self.num_list[lv].pop(self.num_list[lv].index(value))
            if dbg: print("Removed entry "+str(value)+": that entry was used vertically")

    # start_position is a structure [row, col, horizontal]
    def check_write_number(self, row, col, horizontal, value):
        if horizontal:
            return self.check_write_horizontal(row, col, value)
        else:
            return self.check_write_vertical(row, col, value)

    def write_number(self, row, col, horizontal, value):
        if horizontal:
            return self.write_horizontal(row, col, value)
        else:
            return self.write_vertical(row, col, value)

    # Write a number horizontally, return False if conflict
    def check_write_horizontal(self, row, col, value):
        fit = False
        ll = len(value)
        if dbg: print("Writing "+str(value)+" to line "+str(row)+" pos "+str(col)+"], hor_pos="+str(self.grid[row][col].hor_pos)+", len="+str(self.grid[row][col].hor_num_length))
        if self.grid[row][col].hor_pos != 0: return False
        if ll != self.grid[row][col].hor_num_length: return False
        for n in range(ll):
            cell=self.grid[row][col+n]
            if dbg: print("Cell value is "+str(cell.value)+", compared to "+str(value[n]))
            if cell.value != value[n]:
                if cell.value != -1:
                    return False
                # If we are here, it means the cell value is currently empty and we need to
                # check if any horizontal number going through that position with that digit exists
                vpos = self.grid[row][col+n].ver_pos
                # lver is the length of the vertical number
                lver = self.grid[row-vpos][col+n].ver_num_length
                # gather the list of "known" digits and their position for the vertical number
                known=[[vpos, value[n]]]
                for i in range(lver):
                    if self.grid[row-vpos+i][col+n].value != -1:
                        known.append([i, self.grid[row-vpos+i][col+n].value])
                # Now scan every number lver-digit long to see if any would fit
                for i in range(len(self.num_list[lver])):
                    number_to_test = self.num_list[lver][i]
                    # If "fit" remains True after all tests, then it's a fit!
                    fit = True
                    for j in range(len(known)):
                        digit = number_to_test[known[j][0]]
                        if digit != known[j][1]:
                            fit = False
                    if fit:
                        break
                # If one digit doesn't match, stop testing for other digits
                if not fit:
                    return False
        return fit

    def write_horizontal(self, i, j, value):
        for n in range(len(value)):
            self.set_cell_value(i, j+n, value[n])

    # Write a number vertically, return False if conflict
    def check_write_vertical(self, row, col, value):
        fit = False
        ll = len(value)
        if dbg: print("Writing "+str(value)+" to column "+str(col)+" pos "+str(row)+"], ver_pos="+str(self.grid[row][col].ver_pos)+", len="+str(self.grid[row][col].ver_num_length))
        if self.grid[row][col].ver_pos != 0: return False
        if ll != self.grid[row][col].ver_num_length: return False
        for n in range(ll):
            cell=self.grid[row+n][col]
            if dbg: print("Cell value is "+str(cell.value)+", compared to "+str(value[n])+", ll="+str(ll))
            if cell.value != value[n]:
                if cell.value != -1:
                    return False
                # If we are here, it means the cell value is currently empty and we need to
                # check if any horizontal number going through that position with that digit exists
                hpos = self.grid[row+n][col].hor_pos
                # lhor is the length of the horizontal number
                lhor = self.grid[row+n][col-hpos].hor_num_length
                # gather the list of "known" digits and their position for the horizontal number
                known = [[hpos, value[n]]]
                for i in range(lhor):
                    if self.grid[row+n][col-hpos+i].value != -1:
                        known.append([i, self.grid[row+n][col-hpos+i].value])
                # Now scan every number lhor-digit long to see if any would fit
                for i in range(len(self.num_list[lhor])):
                    number_to_test = self.num_list[lhor][i]
                    # If "fit" remains True after all tests, then it's a fit!
                    fit = True
                    for j in range(len(known)):
                        digit = number_to_test[known[j][0]]
                        if digit != known[j][1]:
                            fit = False
                            break
                    if fit:
                        break
                # If one digit doesn't match, stop testing for other digits
                if not fit:
                    return False
        return fit

    def write_vertical(self, i, j, value):
        for n in range(len(value)):
            self.set_cell_value(i+n, j, value[n])

    # Generate the list of start positions of numbers in the grid
    def get_start_positions(self):
        # Reset the list of start positions
        self.start_positions = [[] for i in range(grid_size+1)]
        for i in range(grid_size):
            for j in range(grid_size):
                ll = self.grid[i][j].hor_num_length
                if self.grid[i][j].hor_pos == 0 and self.grid[i][j].num_known_h < ll:
                    self.start_positions[ll].append(Start_cell(i,j,True))
                ll = self.grid[i][j].ver_num_length
                if self.grid[i][j].ver_pos == 0 and self.grid[i][j].num_known_v < ll:
                    self.start_positions[ll].append(Start_cell(i,j,False))
        # Create a list of shortest list of start position to longest
        # start_pos_order is a list of lists [count, index]
        # where count is the number of entries in start_positions[index]
        # and is ordered with the lowest count first.
        # [2, 9] means start_positions[9] has 2 entries of 9 digits
        self.start_pos_order = []
        for i in range(len(self.start_positions)):
            ll = len(self.start_positions[i])
            if ll > 0: self.start_pos_order.append([ll, i])
        if dbg: print(self.start_pos_order)
        for i in range(len(self.start_pos_order) - 1):
            for j in range(i + 1, len(self.start_pos_order)):
                if self.start_pos_order[i][0] > self.start_pos_order[j][0]:
                    self.start_pos_order[i], self.start_pos_order[j] = self.start_pos_order[j], self.start_pos_order[i]
        if dbg: print(self.start_pos_order)
        if dbg:
            for i in range(0, grid_size):
                nb = len(self.start_positions[i])
                if nb>0:
                    print("Start cells for "+str(i)+" char numbers are:")
                    for j in range(0, nb):
                        if self.start_positions[i][j].horizontal:
                            direct="horizontal"
                        else:
                            direct="vertical"
                        print("["+str(self.start_positions[i][j].row)+","+str(self.start_positions[i][j].col)+"]->"+str(direct))


def recurse(g, row, col, hor, value, silent=False):
    # This function will select a position to write a number from the list
    # But writing a number makes it disappear from the list, so it needs first to copy the entire game so if the
    # number wasn't right we can use another one instead
    # We always use entry [0] of start_pos_order
    # start_pos_order entry 0 is something like [2, 9] and it means start_positions[9] has 2 entries of 9 digits
    # start_positions and num_lists have the same structure:
    #   they are lists (rows) of lists, row 4 are for 4-digit numbers
    #   In this loop, we will use the first entry of start_positions for the words with the least entries (and that's the first entry of start_pos_order)
    #   and we will try sequentially all numbers of num_list to fit that location

    # in the first call, dummy values for row, col, etc are used to avoid code repetition
    # The issue is that write_number changes "g" and we don't want that within the loop
    if row != -1:
        g.write_number(row, col, hor, value)
        print("Number "+str(value)+" is being written at position "+str(row)+":"+str(col))
        if not silent:
            print_grid(g)

    g.get_start_positions()
    if len(g.start_pos_order) == 0:
        print("All numbers have been placed!")
        if not silent or dbg:
            print_grid(g, True, True)
        # Return False so if we're looking for another solution, we'll continue assuming that that last value did't work
        return False
    else:
        number_of_entries_of_that_size = g.start_pos_order[0][0]
        number_size = g.start_pos_order[0][1]
        row = g.start_positions[number_size][0].row
        col = g.start_positions[number_size][0].col
        hor = g.start_positions[number_size][0].horizontal

        # Save game features to restore them if writing the word didn't work
        for i in range(0, number_of_entries_of_that_size):
            # Write the number in the grid, and call the recursive loop to fit everything
            # if it eventually returns with False, it means that we should have tried
            # with the next value for
            g2 = g.copy()
            value = g2.num_list[number_size][i]
            word_ok = g2.check_write_number(row, col, hor, value)
            if word_ok:
                recurse(g2, row, col, hor, value)

# Now this function will generate numbers randomly
def generate_number_list(gg):
    global grid_size
    data_not_verified = True
    # Data will be verified when no duplicate exist
    while data_not_verified:
        # Generate random digits in the grid
        for row in range(grid_size):
            for col in range(grid_size):
                if gg.grid[row][col].contains_number:
                    gg.grid[row][col].value = int(random() * 10)

        # Now create the number list from digits in the grid
        # Horizontally first
        gg.num_list=[[] for ll in range(grid_size+1)]
        for row in range(grid_size):
            number = ""
            for col in range(grid_size):
                if gg.grid[row][col].contains_number:
                    number += str(gg.grid[row][col].value)
                else:
                    if number != "":
                        gg.num_list[len(number)].append(number)
                    number = ""
            # If a number finished at the end of a row, we need to store it too
            if number != "":
                gg.num_list[len(number)].append(number)
            number = ""
        # Above created horizontal numbers, we still need to add vertical numbers
        for col in range(grid_size):
            number = ""
            for row in range(grid_size):
                if gg.grid[row][col].contains_number:
                    number += str(gg.grid[row][col].value)
                else:
                    if number != "":
                        gg.num_list[len(number)].append(number)
                    number = ""
            # If a number finished at the end of a column, we need to store it too
            if number != "":
                gg.num_list[len(number)].append(number)
            number = ""
        # Sort numbers
        duplicate_found = False
        for ll in range(len(gg.num_list)):
            gg.num_list[ll].sort()
            for n in range(1, len(gg.num_list[ll])):
                if gg.num_list[ll][n-1] == gg.num_list[ll][n]:
                    duplicate_found = True
                    if dbg:
                        print ("Duplicates found in numbers of "+str(ll)+" digits")
                        for i in range(len(gg.num_list)):
                            print(i, gg.num_list[i])
                    break
            if duplicate_found:
                break
        # If no duplicate found, data is considered verifier
        data_not_verified = duplicate_found
    if dbg:
        print("List of numbers:")
        for ll in range(len(gg.num_list)):
            print (ll, gg.num_list[ll])
    print_grid(gg)

    # Erase the grid and call recurse to find how many solutions exist
    for row in range(grid_size):
        for col in range(grid_size):
            if gg.grid[row][col].contains_number:
                gg.grid[row][col].value = -1

    number_of_solutions = 0
    silent= True # Recurse without any output: we want to count number of solutions
    recurse(gg, -1, -1, -1, -1, silent)

def start_game():
    global grid_size, grid_width, original_game

    original_game = get_file()
    if grid_size >7:
        grid_width = 36*grid_size
    else:
        grid_width = 8*36
    print_grid(original_game)
    # Call recurse with dummy values so I don't have to calculate them here
    recurse(original_game, -1, -1, -1, -1)
    print("After the original recurse")


def design_game():
    def colorflip(x, y, gg):
        global root, grid
        if gg[x][y] == "0":
            gg[x][y] = "#"
            bgcol = "black"
            fgcol = "white"
        else:
            gg[x][y] = "0"
            fgcol = "black"
            bgcol = "white"
        grid[x][y].configure(fg=fgcol, bg=bgcol)

    global root, grid, grid_size, grid_size_max, grid_width, original_game, designed
    min_game_size=6
    max_game_size=20
    designed = True
    root.destroy()
    root = tk.Tk()
    root.title("Design a Fill-Number Game")

    root.geometry("250x200")
    label = tk.Label(root, anchor="center", text="Enter the game size").place(relx=0.5, rely=0.25, anchor="center")
    current_value = tk.StringVar(root)
    spin = tk.Spinbox(root, from_=min_game_size, to=max_game_size, textvariable=current_value).place(relx=0.5, rely=0.5, anchor="center")
    # Note: below I had "destroy" changed for "quit" and the image buttons stopped working!
    tk.Button(root, text="OK", command=lambda: root.destroy()).place(relx=0.2, rely=0.8, anchor="w")
    tk.Button(root, text="Exit", command=lambda: exit()).place(relx=0.8, rely=0.8, anchor="e")
    root.mainloop()
    grid_size = int(current_value.get())

    grid_width = grid_size * 38
    grid_height = (grid_size + 1) * 38
    padding = 0
    if grid_width < 380:
        # If grid is too narrow, the title doesn't display correctly
        grid_width = 380
        # padding is to add some room to the left to center the grid
        padding = ((10 - grid_size) * 19, 0)

    # Now display a grid of the required size made with buttons
    root=tk.Tk()
    root.title("Click on a cell to flip its color")
    root.geometry(str(grid_width) + "x" + str(grid_height))
    fgcol = "black"
    bgcol = "white"
    # "g" is the numbers in the grid, and the grid is initially all numbers
    gg = [ [ "0" for x in range(grid_size)] for y in range(grid_size)]
    grid = [ [ tk.Button(root, text="   ", fg=fgcol, bg=bgcol, command=lambda i=y, j=x: colorflip(i, j, gg)) for x in range(grid_size)] for y in range(grid_size)]
    # Now that the grid has been created, modify its elements to add a command to flip its color
    for x in range(grid_size):
        paddingvalue = padding
        for y in range(grid_size):
            grid[x][y].grid(row=x, column=y, padx=paddingvalue, pady=0)
            paddingvalue = 0
    # And add buttons for OK/Cancel at the bottom
    btn_ok = tk.PhotoImage(file="Button_OK_30.png")
    btn_cancel = tk.PhotoImage(file="Button_Cancel_30.png")
    tk.Button(root, image=btn_ok, command=lambda: root.quit()).grid(row=grid_size+1, column=0, padx=padding, pady=0)
    tk.Button(root, image=btn_cancel, command=lambda: exit()).grid(row=grid_size+1, column=grid_size-1, padx=0, pady=0)
    root.mainloop()
    for i in range(grid_size):
        print(gg[i])
    # Now use "g" to transform "grid" into a grid of cells
    original_game = Game()
    original_game.create_grid(gg)
    original_game.set_hor_ver_pos_in_grid()
    if dbg: print("Grid size = " + str(grid_size))
    generate_number_list(original_game)
    if dbg:
        print(original_game.num_list)

##################################################
##          This is the main routine            ##
##################################################
original_game = Game()

root = tk.Tk()
root.title("Fill-Number Game")
root.geometry("400x200")
tk.Label(root, anchor="center", text="What do you want to do?").place(relx=0.5, rely=0.3, anchor="center")
tk.Button(root, text="Solve", command=lambda: start_game()).place(relx=0.1, rely=0.8, anchor="w")
tk.Button(root, text="Play", command=lambda: interactive_play()).place(relx=0.3, rely=0.8, anchor="w")
tk.Button(root, text="Design a game", command=lambda: design_game()).place(relx=0.6, rely=0.8, anchor="center")
tk.Button(root, text="Exit", command=lambda: exit()).place(relx=0.9, rely=0.8, anchor="e")
root.mainloop()
root.quit()

fgcol = "black"
bgcol = "white"
root=tk.Tk()
root.geometry("300x200")
if designed and number_of_solutions == 1:
    label = tk.Label(root, text="1 solution found after " + str(count) + " iterations\nDo you want to save that game?")
    tk.Button(root, text="Save", fg=fgcol, bg=bgcol, command=lambda x=original_game: save_grid(x)).place(relx=0.1, rely=0.8, anchor="w")
    tk.Button(root, text="Stop", fg=fgcol, bg=bgcol, command=lambda: exit()).place(relx=0.9, rely=0.8, anchor="e")
else:
    if number_of_solutions == 0:
        label = tk.Label(root, text="Found no solution after " + str(count) + " iterations")
    elif number_of_solutions == 1:
        label = tk.Label(root, text="1 solution found after " + str(count) + " iterations")
    else:
        label = tk.Label(root, text=str(number_of_solutions)+" solutions found after "+str(count)+" iterations")
    tk.Button(root, text="Close all", fg=fgcol, bg=bgcol, command=lambda: exit()).place(relx=0.5, rely=0.8, anchor="center")
# Labels are placed the same whatever the case, but buttons are different if "Save" is there
label.place(relx=0.5, rely=0.3, anchor="center")
tk.mainloop()
