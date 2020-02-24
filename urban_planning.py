from common_functions import *
from genetic_algorithm import genetic_algorithm
import hill_climbing_algorithm 
import random
import numpy
import sys

def urban_plan(fname, alg):
    layout = read_File(fname)
    for x in layout[0]:
        print(x)
    if alg == 'GA':
        genetic_algorithm(layout)
    if alg == 'HC':
        read_File = read_File(fname)
        orig_board = read_File[0]
        indust = read_File[1]
        comm = read_File[2]
        resid = read_File[3]
        print("Original board:")
        print(orig_board)
        print("Let's have a nice hill climbing cardio for 10 second...")
        result = hc_annealing(orig_board)
        final_score = result[0]
        first_best_board = result[1]
        first_best_time = round(result[2],3)
        print("At "+ str(first_best_time) + 's, ' + 'we achieved the best score ' + str(final_score) + " on this awsome urban plan: ")
        print(first_best_board)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        urban_plan(sys.argv[1], sys.argv[2])