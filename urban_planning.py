from common_functions import *
import random
import numpy
import sys

def urban_plan(fname, alg):
    layout = read_File(fname)
    rand_solution = gen_rand_solution(layout[0], layout[1], layout[2], layout[3])
    score = score_solution(layout[0], rand_solution)
    for c in rand_solution:
        print(c)
    print(score)
    pass

if __name__ == "__main__":
    if len(sys.argv) == 3:
        urban_plan(sys.argv[1], sys.argv[2])
    pass