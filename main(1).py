
import itertools
import operator
from copy import deepcopy
import time

clauses0=[[1, 2, 3], [4, 5, 6], [7, 8, 9], [-1, -2], [-1, -3], [-2, -3], [-4, -5], [-4, -6], [-5, -6], [-7, -8], [-7, -9], [-8, -9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [-1, -4], [-1, -7], [-4, -7], [-2, -5], [-2, -8], [-5, -8], [-3, -6], [-3, -9], [-6, -9], [1, 8], [-1, -8], [4, 2], [-2, -4]]
[-1, 8, -7, -9, -2, -5, 3, 4, -6]

print('hello')
print(clauses0)


#import wvbw15
#start=time.time()
#print(wvbw15.dpll_sat_solve(clauses0,[]))#