import random
import numpy

# Read a text file and generate a board representation as a 2D array
def read_File(fname):
    board = []
    with open(fname, 'r', encoding='utf-8-sig') as layout:
        for line in layout:
            trantab = str.maketrans(dict.fromkeys(',\n'))
            cleaned_line = line.translate(trantab)
            line_array = [char for char in cleaned_line]
            for x in range(0, len(line_array)):
                if is_intstring(line_array[x]):
                    line_array[x] = int(line_array[x])
            board.append(line_array)
    start_board = fill_board(board)
    return start_board
    pass

# checks the max width of the layout
def check_max(layout):
    max = 0
    for line in layout:
        if len(line) > max:
            max = len(line)
    return max

# checks if the provided index is out of bounds or not
def is_inRange (s, i):
    try:
        b = s[i]
        return True
    except IndexError:
        return False

# checks if the provided string is an int
def is_intstring (s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Given a 2D array layout, homogenizes the width by representing empty spaces as -1
def fill_board(layout):
    max_width = check_max(layout)
    board = []
    i = 0
    for row in layout:
        board.append([])
        for index in range(0, max_width):
            if is_inRange(row, index):
                board[i].append(row[index])
            else:
                board[i].append(-1)
        i+=1
    return board

# Should have 4 possibilities, I - Industrial,  C - Commerce, R - Residential, or no development
def gen_rand_solution(board):
    dev_opt = ['I', 'C', 'R', ' ']
    sol_board = []
    i = 0
    for row in board:
        sol_board.append([])
        for plot in row:
            if plot == -1 or plot == 'X' or plot == 'S':
                sol_board[i].append(plot)
            else:
                sol_board[i].append(dev_opt[random.randint(0, 3)])
        i += 1
    return sol_board

def score_solution(orig_board, sol_board):
    score = 0
    x = 0
    y = 0
    r_coord = find_all_coordinates('R', sol_board)
    c_coord = find_all_coordinates('C', sol_board)
    i_coord = find_all_coordinates('I', sol_board)
    for row in sol_board:
        for plot in row:
            if plot== ' ' or plot == -1:
                score += 0
            elif plot == 'X':
                # Industrial zones within 2 tiles take a penalty of -10
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 10
                # Commercial and residential zones within 2 tiles take a penalty of -20
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 20
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 20
            elif plot == 'S':
                # Residential zones within 2 tiles gain a bonus of 10 points
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score += 10
            elif plot == 'I':
                # For each industrial tile within 2 squares, there is a bonus of 2 points
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score += 2
                score -= 2 + orig_board[y][x]
            elif plot == 'R':
                # For each industrial site within 3 squares there is a penalty of 5 points
                for coord in i_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score -= 5
                # However, for each commercial site with 3 squares there is a bonus of 4 points
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score += 4
                score -= 2 + orig_board[y][x]
            elif plot == 'C':
                # For each residential tile within 3 squares, there is a bonus of 4 points
                for coord in r_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=3:
                        score += 4
                # For each commercial site with 2 squares, there is a penalty of 4 points
                for coord in c_coord:
                    dist = abs(abs(coord[0] - y) + abs(coord[1] - x))
                    if dist <=2:
                        score -= 4
                score -= 2 + orig_board[y][x]
            x += 1
        x = 0
        y += 1
    return score

def find_all_coordinates(building, board):
    coordinates = []
    y = 0
    x = 0
    for row in board:
        for plot in row:
            if plot == building:
                coordinates.append((y, x))
            x += 1
        x = 0
        y += 1
    return coordinates