#!/usr/bin/python3
import tkinter as tk

dbg=False
maxNum = 0
count = 0

def print_grid(grid_size, grid_of_cells, pause=False, solution=False):
    global count
    count += 1
    if pause or count % 10 == 0:
        root = tk.Tk()
        if solution:
            root.title(f"Solution found after {count} attempts")
        else:
            root.title(f"Fill Numbers Game - {count}")
        root.geometry("500x500")

        for i in range(grid_size):
            for j in range(grid_size):
                tx = " "
                if grid_of_cells[i][j].contains_number:
                    fgcol = "black"
                    bgcol = "white"
                    if grid_of_cells[i][j].value != -1:
                        tx = grid_of_cells[i][j].value
                else:
                    fgcol = "white"
                    bgcol = "black"
                tk.Button(root, text=tx, fg=fgcol, bg=bgcol).grid(row=i, column=j, padx=0, pady=0)
        if pause:
            root.mainloop()
        else:
            root.update()


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
    def __init__(self, filename="Numbers.txt"):
        # xy is an array of up to 13 lines and columns and each entry contains a Cell
        global dbg
        self.grid_size = 13
        # Grid is up to grid_size x grid_size
        # It comprises grid_size lines, and each line is a list of cells
        self.xy = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        # num_list is the list of numbers to fit in the grid
        self.num_list = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        # start_positions is the list of x-y coordinates where a horizontal or vertical number starts
        self.start_positions = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        # start_pos_order is a list of lists [count, index]
        # where count is the number of entries in start_positions[index]
        # and is ordered with the lowest count first.
        # [2, 9] means start_positions[9] has 2 entries of 9 digits
        self.start_pos_order = []
        # Initialize the whole grid as an array of black cells
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.xy[i].append(Cell())
        # Use the grid to change black cells into number cells and set the horizontal pos in the number
        if dbg: print(f"Creating the Game grid with size {self.grid_size} x {self.grid_size}")
        self.read_grid(filename)
        if dbg: print(f"Grid size = {self.grid_size}")
        for i in range(self.grid_size):
            h=0
            for j in range(self.grid_size):
                if self.xy[i][j].contains_number:
                    self.xy[i][j].set_hor_pos(h)
                    h+=1
                else:
                    h=0
        for j in range(self.grid_size):
            v=0
            for i in range(self.grid_size):
                if self.xy[i][j].contains_number:
                   self.xy[i][j].set_ver_pos(v)
                   v += 1
                else:
                   v = 0
        # Set number length horizontally
        for i in range(self.grid_size):
            h=0
            for j in range(self.grid_size-1,-1,-1):
                if self.xy[i][j].contains_number:
                    if h == 0: h = self.xy[i][j].hor_pos+1
                    self.xy[i][j].set_hor_num_length(h)
                else:
                    h=0
        # Set number length vertically
        for j in range(self.grid_size):
            v=0
            for i in range(self.grid_size-1,-1,-1):
                if self.xy[i][j].contains_number:
                    if v == 0: v = self.xy[i][j].ver_pos+1
                    self.xy[i][j].set_ver_num_length(v)
                else:
                    v=0
        if dbg:
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    print(f"[{i}:{j}]: contains_number={self.xy[i][j].contains_number}, HorNumLen: {self.xy[i][j].hor_num_length}, HorPos: {self.xy[i][j].hor_pos}, VerNumLen: {self.xy[i][j].ver_num_length}, VerPos: {self.xy[i][j].ver_pos}")

    def copy_xy(self):
        nouveau_xy = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        for i in range(len(self.xy)):
            for j in range(len(self.xy[i])):
                nouveau_xy[i].append(self.xy[i][j].copy())
        return nouveau_xy

    def copy_num_list(self):
        nouveau_list = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        for i in range(len(self.num_list)):
            for j in range(len(self.num_list[i])):
                nouveau_list[i].append(self.num_list[i][j])
        return nouveau_list

    def read_grid(self, filename: "Numbers.txt") -> bool:
        reading_numbers = True
        num_digits = 0
        num_cases = 0
        gridline = 0
        file = open(filename, "r")
        line = file.readline().strip()
        length = len(line)
        while length > 0:
            if reading_numbers:
                if line != "GRID":
                    if dbg: print(f"{length}-digit number: <{line}>")
                    self.num_list[length].append(line)
                    num_digits += length
                    if length > self.grid_size:
                        print(f"Number too long ({length})\nMaximum length of numbers set to {maxNum}")
                        return False
                else:
                    reading_numbers = False
            else:
                if dbg: print(f"Grid: <{line}>")
                for i in range(length):
                    if line[i] == "0":
                        if dbg: print(f"[{gridline},{i}]: Contains_Number")
                        self.xy[gridline][i].contains_number = True
                        num_cases += 1
                    else:
                        if dbg: print(f"[{gridline},{i}]: Not a Number")
                        self.xy[gridline][i].contains_number = False
                gridline += 1
            line = file.readline().strip()
            length = len(line)
        if num_cases * 2 != num_digits:
            print(
                f"Error in the file: {num_digits} digits should be an even number and should be equal to 2* number of cases (={num_cases})")
            return False
        else:
            print(f"\nFile OK: {num_digits} digits fit correctly in {num_cases} cases: 2*{num_cases}={num_digits}")
            return True

    def set_cell_value(self, i, j, v):
        # When setting a cell value, it also increments the number of known letters of vertical and horizontal numbers
        c = self.xy[i][j]
        if dbg:
            print(f"Setting cell [{i},{j}] to value {v}")
        # the value is already set, nothing to do
        if c.value == v: return
        c.value = v

        # self.grid[i] = self.grid[i][0:j]+v+self.grid[i][j+1:]
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
        if dbg: print(f"Writing {value} to line {row} pos {col}], hor_pos={self.xy[row][col].hor_pos}, len={self.xy[row][col].hor_num_length}")
        if self.xy[row][col].hor_pos != 0: return False
        if ll != self.xy[row][col].hor_num_length: return False
        for n in range(ll):
            cell=self.xy[row][col+n]
            if dbg: print(f"Cell value is {cell.value}, compared to {value[n]}")
            if cell.value != value[n]:
                if cell.value != -1:
                    return False
                # If we are here, it means the cell value is currently empty and we need to
                # check if any horizontal number going through that position with that digit exists
                vpos = self.xy[row][col+n].ver_pos
                # lver is the length of the vertical number
                lver = self.xy[row-vpos][col+n].ver_num_length
                # gather the list of "known" digits and their position for the vertical number
                known=[[vpos, value[n]]]
                for i in range(lver):
                    if self.xy[row-vpos+i][col+n].value != -1:
                        known.append([i, self.xy[row-vpos+i][col+n].value])
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
        if dbg: print(f"Writing {value} to column {col} pos {row}], ver_pos={self.xy[row][col].ver_pos}, len={self.xy[row][col].ver_num_length}")
        if self.xy[row][col].ver_pos != 0: return False
        if ll != self.xy[row][col].ver_num_length: return False
        for n in range(ll):
            cell=self.xy[row+n][col]
            if dbg: print(f"Cell value is {cell.value}, compared to {value[n]}, ll={ll}")
            if cell.value != value[n]:
                if cell.value != -1:
                    return False
                # If we are here, it means the cell value is currently empty and we need to
                # check if any horizontal number going through that position with that digit exists
                hpos = self.xy[row+n][col].hor_pos
                # lhor is the length of the horizontal number
                lhor = self.xy[row+n][col-hpos].hor_num_length
                # gather the list of "known" digits and their position for the horizontal number
                known = [[hpos, value[n]]]
                for i in range(lhor):
                    if self.xy[row+n][col-hpos+i].value != -1:
                        known.append([i, self.xy[row+n][col-hpos+i].value])
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
        self.start_positions = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        for i in range(0, self.grid_size):
            for j in range(0, self.grid_size):
                ll = self.xy[i][j].hor_num_length
                if self.xy[i][j].hor_pos == 0 and self.xy[i][j].num_known_h < ll:
                    self.start_positions[ll].append(Start_cell(i,j,True))
                ll = self.xy[i][j].ver_num_length
                if self.xy[i][j].ver_pos == 0 and self.xy[i][j].num_known_v < ll:
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
            for i in range(0, self.grid_size):
                nb = len(self.start_positions[i])
                if nb>0:
                    print(f"Start cells for {i} char numbers are:")
                    for j in range(0, nb):
                        if self.start_positions[i][j].horizontal:
                            direct="horizontal"
                        else:
                            direct="vertical"
                        print(f"[{self.start_positions[i][j].row},{self.start_positions[i][j].col}]->{direct}")

def recurse(g, row, col, hor, value):
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
        print(f"Number {value} is being written at position {row}:{col}")
        print_grid(g.grid_size, g.xy)

    if value == '910850811':
        print_grid(g.grid_size, g.xy, True)
    g.get_start_positions()
    if len(g.start_pos_order) == 0:
        print("All numbers have been placed!")
        print_grid(g.grid_size, g.xy, True, True)
    else:
        number_of_entries_of_that_size = g.start_pos_order[0][0]
        number_size = g.start_pos_order[0][1]
        row = g.start_positions[number_size][0].row
        col = g.start_positions[number_size][0].col
        hor = g.start_positions[number_size][0].horizontal

        # Save game features to restore them if writing the word didn't work
        g2 = Game()
        g2.grid_size = g.grid_size
        for i in range(0, number_of_entries_of_that_size):
            # Write the number in the grid, and call the recursive loop to fit everything
            # if it eventually returns with False, it means that we should have tried
            # with the next value for
            g2.num_list = g.copy_num_list()
            g2.xy = g.copy_xy()
            g2.get_start_positions()
            value = g2.num_list[number_size][i]
            word_ok = g2.check_write_number(row, col, hor, value)
            if word_ok:
                recurse(g2, row, col, hor, value)

def debug_data():
    global g
    for i in range(0,4):
        for j in range(0,4):
            print(f"[{i},{j}]: HorPos={g.xy[i][j].hor_pos}, VerPos={g.xy[i][j].ver_pos}, Value={g.xy[i][j].value}")

NumWordsPlaced=0
NumWordsPlacedMax=0
g=Game("Numbers.txt")
print_grid(g.grid_size, g.xy)
# Call recurse with dummy values so I don't have to calculate them here
recurse(g, -1, -1, -1, -1)

print("Done")

