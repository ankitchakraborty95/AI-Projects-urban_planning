from common_functions import *
import random
import numpy
import sys

def urban_plan(fname, alg):
    layout = read_File(fname)
    rand_solution = gen_rand_solution(layout)
    score = score_solution(layout, rand_solution)
    for x in rand_solution:
        print(x)
    print(score)
    pass

if __name__ == "__main__":
    if len(sys.argv) == 3:
        urban_plan(sys.argv[1], sys.argv[2])
    pass