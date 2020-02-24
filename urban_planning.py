from common_functions import *
from genetic_algorithm import genetic_algorithm
from hill_climbing_algorithm import *
import random
import numpy
import sys

def urban_plan(fname, alg):
    layout = read_File(fname)
    print("Initial Board")
    for x in layout[0]:
        print(x)
    if alg == 'GA':
        genetic_algorithm(layout)
    if alg == 'HC':
        orig_board = layout[0]
        indust = layout[1]
        comm = layout[2]
        resid = layout[3]
        result = hc_annealing(orig_board, indust, comm, resid)
        final_score = result[0]
        first_best_board = result[1]
        first_best_time = round(result[2],3)
        print("At "+ str(first_best_time) + 's, ' + 'we achieved the best score ' + str(final_score) + " on this awsome urban plan: ")
        for x in first_best_board:
            print(x)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        urban_plan(sys.argv[1], sys.argv[2])