from random import randint, sample
from scipy import sparse
from scipy.special import expit
import numpy as np

n_nodes = 10


test = sparse.lil_matrix((n_nodes, n_nodes))

indexes = np.array(sample(range(n_nodes), 5))

test[0, 1] = 1

vec = np.random.normal(1,1,n_nodes)

print(vec)

out = test.dot(vec)

print(expit(out))
