# import collections
import numpy as np

# ALL_INPUTS = collections.namedtuple('ALL_INPUTS', 'light oncoming left right')

# inputs = ALL_INPUTS(light = 'green', oncoming = None, left = None, right = None)

# print ALL_INPUTS
# light, oncoming, left, right = inputs

# print inputs['light']

# number of states
nS = 64
# number of actions
nA = 3
P_rand = np.random.rand(nS, nA, nS)
print P_rand