import random
import copy
import time
from common_functions import *
pop_size = 400
elitism_factor = 40
culling_factor = 8
time_limit = 10.0

# main genetic algorithm
def genetic_algorithm(ref_layout):
    start_time = time.perf_counter()
    input_board = ref_layout
    initial_pop = gen_population(input_board, pop_size)
    curr_pop = copy.deepcopy(initial_pop)

    run = True
    while (run):
        elitism_pop = get_parents(curr_pop, elitism_factor)
        next_gen_pop = []
        #######elitism pop############
        for x in elitism_pop:
            next_gen_pop.append(x)
        #########pop after culling#########33
        pop_after_culling = culling_pop(curr_pop, culling_factor)
        children_count = pop_size - elitism_factor
        i = 0
        while (children_count > 0):
            if (children_count != 1):
                child = create_children_2(input_board[0], pop_after_culling[i][0], pop_after_culling[i + 1][0])
                next_gen_pop.append(child[0])
                next_gen_pop.append(child[1])
                i = i + 2
                children_count = children_count - 2
            else:
                child = create_children_2(input_board[0], pop_after_culling[i][0], pop_after_culling[i + 1][0])
                next_gen_pop.append(child[0])
                i = i + 1
                children_count = children_count - 1
        curr_pop = next_gen_pop
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        if (time_limit-0.1 < execution_time <= time_limit+0.1):
            print("execution time", execution_time)
            run = False

    get_best_fit(curr_pop)
    print("best score found")
    for x in curr_pop[0][0]:
        print(x)
    print(curr_pop[0][1])

def create_children_2(reference,mom,dad):
    reference_copy = copy.deepcopy(reference)
    mom_copy = copy.deepcopy(mom)
    dad_copy = copy.deepcopy(dad)
    child1 =copy.deepcopy(reference_copy)
    child2 =copy.deepcopy(reference_copy)
    i_temp_mom = find_all_coordinates('I',mom_copy)
    i_temp_dad= find_all_coordinates('I', dad_copy)
    n = random.randint(0,1)
    if(n==0):
        for cord in i_temp_mom:
            child1[cord[0]][cord[1]] = 'I'
        for cord in i_temp_dad:
            child2[cord[0]][cord[1]] = 'I'
    else:
        for cord in i_temp_dad:
            child1[cord[0]][cord[1]] = 'I'
        for cord in i_temp_mom:
            child2[cord[0]][cord[1]] = 'I'
#############################################
    c_temp_mom = find_all_coordinates('C', mom_copy)
    c_temp_dad = find_all_coordinates('C', dad_copy)
    n = random.randint(0, 1)
    if (n == 0):
        for cord in c_temp_mom:
            child1[cord[0]][cord[1]] = 'C'
        for cord in c_temp_dad:
            child2[cord[0]][cord[1]] = 'C'
    else:
        for cord in c_temp_dad:
            child1[cord[0]][cord[1]] = 'C'
        for cord in c_temp_mom:
            child2[cord[0]][cord[1]] = 'C'

##################################################3
    r_temp_mom = find_all_coordinates('R', mom_copy)
    r_temp_dad = find_all_coordinates('R', dad_copy)
    n = random.randint(0, 1)
    if (n == 0):
        for cord in r_temp_mom:
            child1[cord[0]][cord[1]] = 'R'
        for cord in r_temp_dad:
            child2[cord[0]][cord[1]] = 'R'
    else:
        for cord in r_temp_dad:
            child1[cord[0]][cord[1]] = 'R'
        for cord in r_temp_mom:
            child2[cord[0]][cord[1]] = 'R'

    while(check_board(child1)==False):
        mutate_board(child1)
    while (check_board(child2) == False):
        mutate_board(child2)
    # Randomly mutate a child with 10% chance
    try_mutate = random.randint(0, 100)
    if(try_mutate<=0):
        n = random.randint(0, 1)
        if(n==0):
            child1 = gen_mutation(reference, child1)
        else:
            child2 = gen_mutation(reference, child2)
    child1_score = score_solution(reference_copy, child1)
    child2_score = score_solution(reference_copy, child2)
    return [(child1, child1_score), (child2, child2_score)]


def check_board(board):
    r_coord = find_all_coordinates('R', board)
    c_coord = find_all_coordinates('C', board)
    i_coord = find_all_coordinates('I', board)
    if(len(r_coord)==0 or len(i_coord)==0 or len(c_coord)==0):
        return False
    else:
        return True

# Moves a building to another coordinate
def gen_mutation(ref, board):
    new_board = [plot[:] for plot in ref]
    height = len(board) - 1
    width = len(board[0]) - 1
    rand_height = random.randint(0, height)
    rand_width = random.randint(0, width)
    while not is_intstring(board[rand_height][rand_width]):
        rand_height = random.randint(0, height)
        rand_width = random.randint(0, width)
    n = random.randint(0, 2)
    i_coord = find_all_coordinates('I', board)
    c_coord = find_all_coordinates('C', board)
    r_coord = find_all_coordinates('R', board)
    if(n == 0):
        m = random.randint(0, len(i_coord)-1)
        for x in range(0, len(i_coord)):
            if m == x:
               new_board[rand_height][rand_width] = 'I'
            else:
                old_indus = i_coord[x]
                new_board[old_indus[0]][old_indus[1]] = 'I'
        for comm in c_coord:
            new_board[comm[0]][comm[1]] = 'C'
        for resid in r_coord:
            new_board[resid[0]][resid[1]] = 'R'
    elif n == 1:
        for indus in i_coord:
            new_board[indus[0]][indus[1]] = 'I'
        m = random.randint(0, len(c_coord) - 1)
        for x in range(0, len(c_coord)):
            if m == x:
                new_board[rand_height][rand_width] = 'C'
            else:
                old_comm = c_coord[x]
                new_board[old_comm[0]][old_comm[1]] = 'C'
        for resid in r_coord:
            new_board[resid[0]][resid[1]] = 'R'
    else:
        for comm in c_coord:
            new_board[comm[0]][comm[1]] = 'C'
        for indus in i_coord:
            new_board[indus[0]][indus[1]] = 'I'
        m = random.randint(0, len(r_coord) - 1)
        for x in range(0, len(r_coord)):
            if m == x:
                new_board[rand_height][rand_width] = 'R'
            else:
                old_resid = r_coord[x]
                new_board[old_resid[0]][old_resid[1]] = 'R'
    return new_board

def mutate_board(board):
    i_cord = find_all_coordinates('I',board)
    if(len(i_cord)==0):
        t = True
        while(t):
            row = random.randint(0,(len(board)-1))
            col = random.randint(0,(len(board[0])-1))
            if(board[row][col]!='X' and board[row][col]!='S' and board[row][col]!='C' and board[row][col]!='R'):
                board[row][col]='I'
                t=False
    c_cord = find_all_coordinates('C', board)
    if (len(c_cord) == 0):
        t = True
        while (t):
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board[0]) - 1)
            if (board[row][col] != 'X' and board[row][col] != 'S' and board[row][col] != 'I' and board[row][
                col] != 'R'):
                board[row][col] = 'C'
                t = False
    r_cord = find_all_coordinates('R', board)
    if (len(r_cord) == 0):
        t = True
        while (t):
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board[0]) - 1)
            if (board[row][col] != 'X' and board[row][col] != 'S' and board[row][col] != 'I' and board[row][
                col] != 'C'):
                board[row][col] = 'R'
                t = False
    return board
