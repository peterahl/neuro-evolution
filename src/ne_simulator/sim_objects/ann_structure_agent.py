import itertools

import numpy as np
from scipy.special import expit
from scipy.sparse import lil_matrix
from random import sample
from random import randint

from .empty import Empty
from .food import Food
from .sim_agent import SimAgent
from .sim_object import SimObject
from .wall import Wall


np.set_printoptions(precision=2)

_OBJECT_TO_INPUT = {
    Wall.SYMBOL: (1, 0, 0), Empty.SYMBOL: (0, 1, 0), Food.SYMBOL: (0, 0, 1)}

_MAX_ENERGY = 1.0

_ENERGY_LEVELS = 5

# Fields front, left, right, energy level and last action ok
_NUMBER_OF_INPUTS = len(_OBJECT_TO_INPUT) * 3 + _ENERGY_LEVELS

_OUTPUT_INDEX_TO_ACTION = {
    0: SimObject.Action.MOVE,
    1: SimObject.Action.EAT,
    2: SimObject.Action.TURN_LEFT,
    3: SimObject.Action.TURN_RIGHT,
    4: SimObject.Action.DO_NOTHING
}


def _connect_all_to_all(sources, targets, weight_matrix):
    """ Adds all to all connectivity for network between sources and targets
        with random values. row = target, col = source (to work with
        multiplication later"""
    for s in sources:
        for t in targets:
            weight_matrix[t][s] = np.random.random()

def _create_sparse_wheight_matrix(ann_configuration):
    n_nodes = ann_configuration['num_nodes']

def _max_index(input_vector):
    max_value = 0
    max_index = 0
    for i, element in enumerate(input_vector):
        if element > max_value:
            max_value = element
            max_index = i
    return max_index


def _energy_conversion(energy):
    energy_index = round(energy * (_ENERGY_LEVELS - 1) / _MAX_ENERGY)
    return [1 if i == energy_index else 0 for i in range(_ENERGY_LEVELS)]

def _initialize_structure():
    num_cols = 4
    num_layers = 4
    for col in num_cols:
        for layer in num_layers:
            mu = np.random.normal(0, 0.3)
            sigma = 0.1
            num_nodes = randint(4,10)
            out_degree = randint(num_nodes, num_nodes * 2)
            local_contections = sample(

            

class ANNSimpleAgent(SimAgent):

    WEIGHTS_KEY = 'weights'

    def __init__(self, context, *args, **kwds):
        super().__init__(context, *args, **kwds)
        self._n_layers = kwds.get('n_layers', 3)
        self._n_inputs = _NUMBER_OF_INPUTS
        self._n_middle = 4  # number of units in middle layer
        self._n_outputs = len(_OUTPUT_INDEX_TO_ACTION)
        self._n_nodes = self._n_inputs + self._n_middle + self._n_outputs
        self._node_values = np.array([0]*self._n_nodes)
        self._energy = _MAX_ENERGY
        self._binary_input = [0, ] * _NUMBER_OF_INPUTS
        weights = self._ctx.get(self.WEIGHTS_KEY)
        if weights is not None:
            weights = np.array(weights)
        else:
            weights = self.set_random_weights_three_layer_network()
            self._ctx[self.WEIGHTS_KEY] = [list(w) for w in weights]
        self._weights = weights

    def set_random_weights_three_layer_network(self):
        """ just something simple to create a weight matrix
            for a three layer network"""

        n_nodes = self._n_inputs + self._n_outputs + self._n_middle
        weights = np.zeros([n_nodes, n_nodes])
        nodes = list(range(n_nodes))
        layer1 = nodes[:self._n_inputs]
        layer2 = nodes[self._n_inputs:self._n_inputs + self._n_middle]
        layer3 = nodes[-self._n_outputs:]

        _connect_all_to_all(layer1, layer2, weights)
        _connect_all_to_all(layer2, layer3, weights)

        # print("--------WEIGHT MATRIX--------------")
        # print(self._weights)
        
        return weights

    def start_turn(self, objects_map):
        super().start_turn(objects_map)
        # Reduce energy.
        self._energy -= 0.01  # do not monitor this
        if self._energy <= 0.0001:
            self._action = self.Action.DIE
        else:
            visible = self.get_visible(objects_map)
            """create binary input vector"""
            """!right now ONLY what the agent 'sees', not 'effect of actions' or
            energy
            """
            binary_input = [
                _OBJECT_TO_INPUT[f.SYMBOL] for f in visible]
            binary_input = list(itertools.chain.from_iterable(binary_input))
            # print("binary input: ", binary_input)
            self._set_inputs(binary_input)

            """ Run network for as many steps as layers"""
            for _ in range(self._n_layers-1):
                self._step()

            """convert from binary to correct output format"""
            output = self._get_outputs()
            # print(output)
            ind = _max_index(output)
            # print("Max output index", _OUTPUT_INDEX_TO_ACTION[ind])
            self._action = _OUTPUT_INDEX_TO_ACTION[ind]

    def _set_inputs(self, values):
        self._node_values[:self._n_inputs] = (
            values + _energy_conversion(self._energy))

    def _step(self):
        self._node_values = expit(np.dot(self._weights, self._node_values))
        # self._pretty_print_values(self._node_values)

    def _get_outputs(self):
        return self._node_values[-self._n_outputs:]

    def setweights(self, new_weights):
        self._weights = new_weights

    def _pretty_print_values(self, values):
        """For debugging, hardcoded three layer network"""
        print('----------------------------')
        print("Input", str(values[:self._n_inputs]))
        print("Middle", values[self._n_inputs:-self._n_outputs])
        print("Output", values[-self._n_outputs:])
        print('----------------------------')

ANNSimpleAgent.register()
