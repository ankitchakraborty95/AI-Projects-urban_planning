from common_functions import *
from genetic_algorithm import genetic_algorithm
import random
import numpy
import sys

def urban_plan(fname, alg):
    layout = read_File(fname)
    if alg == 'GA':
        genetic_algorithm(layout)
    pass

if __name__ == "__main__":
    if len(sys.argv) == 3:
        urban_plan(sys.argv[1], sys.argv[2])
    pass