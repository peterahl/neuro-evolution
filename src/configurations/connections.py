from numpy.random import choice
from numpy import array
from random import sample
from math import floor, ceil

mean = 4.9
n_projecting_nodes = 10
low = int(floor(mean))
high = int(ceil(mean))
pl = high - mean
ph = 1 - pl

array(choice([low, high], n_projecting_nodes, p=[pl, ph]), dtype=int)
