# -*- coding: utf-8 -*-
from itertools import chain
from math import floor, ceil
from random import randint, random, sample
from scipy import sparse
from scipy.special import expit

import numpy as np

from .empty import Empty
from .food import Food
from .sim_agent import SimAgent
from .sim_object import SimObject
from .wall import Wall


_OBJECT_TO_INPUT = {
    Wall.SYMBOL: (1, 0, 0), Empty.SYMBOL: (0, 1, 0), Food.SYMBOL: (0, 0, 1)}

_MAX_ENERGY = 1.0

_ENERGY_LEVELS = 5

_FRAC = 7

_SHIFT = 3

# Fields front, left, right, energy level and last action ok
_N_INPUT_UNITS = len(_OBJECT_TO_INPUT) * 3 + _ENERGY_LEVELS

_OUTPUT_INDEX_TO_ACTION = (
    SimObject.Action.MOVE,
    SimObject.Action.EAT,
    SimObject.Action.TURN_LEFT,
    SimObject.Action.TURN_RIGHT,
    SimObject.Action.DO_NOTHING
)

_N_OUTPUT_UNITS = len(_OUTPUT_INDEX_TO_ACTION) - 1

_INITIAL_UNITS = 1

_INITIAL_MIN_NODES = 8

_INITIAL_MAX_NODES = 14

_INITIAL_LAYERS_MIN = 3

_INITIAL_LAYERS_MAX = 6

_INITIAL_MU_RANGE = 0.5

_INITIAL_SIGMA = 0.3

_INITIAL_OUTDEGREE_MIN = 1

_INITIAL_OUTDEGREE_MAX = 4

_INITIAL_PROJECTIONS_PER_LAYER = 2


def _energy_conversion(energy):
    energy_index = round(energy * (_ENERGY_LEVELS - 1) / _MAX_ENERGY)
    return [1 if i == energy_index else 0 for i in range(_ENERGY_LEVELS)]


def _max_index(input_vector):
    max_value = 0
    max_index = 0
    for i, element in enumerate(input_vector):
        if element > max_value:
            max_value = element
            max_index = i
    # print(max_index, max_value)
    if max_value > 0.01:
        return max_index
    return -1


def _rand_range(rng):
    return random() * 2 * rng - rng


def _create_initial_structure():
    """Create the inital randomized structure for the agent.

    For the structure, see the ANNStructuredAgent configuration below.

    """
    # seed(11)
    # Create units (populations or columns) and layers with their nodes count.
    structure = [
        [(randint(_INITIAL_MIN_NODES, _INITIAL_MAX_NODES), {})
            for _ in range(randint(_INITIAL_LAYERS_MIN, _INITIAL_LAYERS_MAX))]
        for _ in range(_INITIAL_UNITS)
    ]

    structure[0][0] = (_N_INPUT_UNITS, {})
    structure[-1][-1] = (_N_OUTPUT_UNITS, {})

    # For each layer in each unit: add the configuration (connections).

    for j, unit in enumerate(structure):
        for i, (unused_num_nodes, conns) in enumerate(unit):
            # Connect this layer to other layers in the same unit.

            # connect to n number of random layers
            # others = sample(
            #     [n for n in range(len(unit)) if n != 0],
            #     _INITIAL_PROJECTIONS_PER_LAYER)

            # connect to all but self and input units
            others = [n for n in range(1, len(unit)) if n != i]

            for o in others:
                conns[o] = (
                    _rand_range(_INITIAL_MU_RANGE), _INITIAL_SIGMA,
                    randint(_INITIAL_OUTDEGREE_MIN, _INITIAL_OUTDEGREE_MAX))

            # Connect the last layer of the current unit to other units.

            if i == len(unit) - 1 and j < len(structure) - 1:
                others = [n for n in range(len(structure)) if n != j]
                conns_to_layer = {
                    n: (abs(_rand_range(_INITIAL_MU_RANGE)), _INITIAL_SIGMA,
                        randint(
                            _INITIAL_OUTDEGREE_MIN, _INITIAL_OUTDEGREE_MAX))
                    for n in others}
                conns[None] = conns_to_layer

    return structure


def _node_index(nodes, to_layer):
    # print(to_layer)
    start = sum(nodes[:to_layer])
    stop = start + nodes[to_layer]
    return list(range(start, stop))


def _projections(out_degree=4.4, n_projecting_nodes=10):
    low = int(floor(out_degree))
    high = int(ceil(out_degree))
    pl = high - out_degree
    ph = 1 - pl
    return np.array(
        np.random.choice(
            [low, high], n_projecting_nodes, p=[pl, ph]),
        dtype=int)


def _create_matrix(structure):

    nodes_per_layer = list(
        chain.from_iterable([[i[0] for i in j] for j in structure]))
    n_nodes = sum(nodes_per_layer)
    print(n_nodes)
    layers_per_unit = [len(unit) for unit in structure]

    accum_layers_per_unit = [
        sum(layers_per_unit[0:i]) for i in range(len(layers_per_unit))]

    wheight_matrix = sparse.lil_matrix((n_nodes, n_nodes))
    wheight_matrix_normal = np.zeros((n_nodes, n_nodes))

    for j, unit in enumerate(structure):
        for i, (num_nodes, conns) in enumerate(unit):
            from_nodes = _node_index(
                nodes_per_layer, i + accum_layers_per_unit[j])

            others = conns.keys()

            for o in others:
                if o:
                    to_layer = o + accum_layers_per_unit[j]
                    # print(
                    #     "from " + str(from_nodes) + " to layer: " +
                    #     str(to_layer))
                    for from_node, n_projections in zip(
                            from_nodes, _projections(conns[o][2], num_nodes)):
                        for to_node in np.random.choice(
                                _node_index(nodes_per_layer, to_layer),
                                n_projections):
                            wheight = np.random.normal(
                                conns[o][0], conns[o][1], 1)[0]
                            wheight_matrix[to_node, from_node] = wheight
                            wheight_matrix_normal[to_node][from_node] = wheight
                else:
                    # this happens if other (o) is none
                    conns_to_layer = conns[o]
                    for to_unit in conns_to_layer.keys():
                        if to_unit:
                            to_layer = accum_layers_per_unit[to_unit]
                            for from_node, n_projections in zip(
                                    from_nodes,
                                    _projections(
                                        conns_to_layer[to_unit][2],
                                        num_nodes)):

                                for to_node in np.random.choice(
                                        _node_index(nodes_per_layer, to_layer),
                                        n_projections):

                                    wheight = np.random.normal(
                                        conns_to_layer[to_unit][0],
                                        conns_to_layer[to_unit][1], 1)[0]
                                    wheight_matrix[to_node, from_node] = (
                                        wheight)
                                    (wheight_matrix_normal[to_node]
                                        [from_node]) = wheight

    return wheight_matrix, wheight_matrix_normal, n_nodes


class ANNStructuredAgent(SimAgent):
    """Agent that evolves its structure but generates the weights anew each
    simulation (generation).

    Structure definition:
    structure = *unit
    unit = *(number_of_nodes connections)
    connections = *connection
    connection = (to_layer_index : (weights_mu weights_sigma out_degree)) /
        (None : to_unit_connections)
    to_unit_connections = *to_unit_connection
    to_unit_connection = to_unit_index : (weights_mu weights_sigma out_degree)

    The layer with index 0 is regarded the input layer, with index -1 it is the
    output layer. This implies that at least two layers have to exist, always.

    Layer -1 can then connect to any number of other units (layer 0 therein).

    For example two units with 2 and 3 layers and with 4 nodes each, no
    connections:
        [[(4, {}), (4, {})], [(4, {}), (4, {}), (4, {})]]
    Adding connections it becomes more like this:
        [[  # unit 0 definition
            (4, {1: (0.2, 0.3, 3.1)},  # connect layer 0 to 1
            (4, {
                0: (-0.1, 0.2, 2.5),   # connect layer 1 to 0
                None: {1: (0.1, 0.3, 3.5)}  # connect unit 0 to unit1
        ], [  # unit 1 definition
            ...
        ]]
    """

    MIN_MAX_KEY = "min_max"

    MIN_MAX_TEMPLATE = {
        # min, max, lower, upper, delta
        "nodes": (8, 14, 2.0, 20.0, 1.0),
        "layers": (3, 6, 2.0, 10.0, 0.3),
        "mu": (0.4, 0.5, 0.0, 1.0, 0.01),
        "sigma": (0.25, 0.3, 0.2, 0.5, 0.001),
        "outdegree": (1, 4, 1.0, 15.0, 0.3)
    }

    def __init__(self, context, *args, **kwds):
        super().__init__(context, *args, **kwds)
        # Get or set the structure.
        # structure = self._ctx.get(self.STRUCTURE_KEY)
        # if structure is None:
        #     structure = _create_initial_structure()
        #     self._ctx[self.STRUCTURE_KEY] = structure
        # TODO: generate weights.
        self._energy = _MAX_ENERGY
        structure = _create_initial_structure()
        self._wheight_matrix, _, n_nodes = (
            _create_matrix(structure))
        self._nodes = np.zeros(n_nodes)

    def start_turn(self, objects_map):
        super().start_turn(objects_map)
        # Reduce energy.
        self._energy -= 0.01  # do not monitor this
        if self._energy <= 0.0001:
            self._action = self.Action.DIE
        else:
            visible = self.get_visible(objects_map)
            binary_input = [
                _OBJECT_TO_INPUT[f.SYMBOL] for f in visible]
            binary_input = list(chain.from_iterable(binary_input))
            binary_input.extend(_energy_conversion(self._energy))

            self._nodes[0:_N_INPUT_UNITS] = binary_input
            for _ in range(5):
                self._nodes = expit(
                    self._wheight_matrix.dot(self._nodes) * _FRAC - _SHIFT)
                self._nodes[0:_N_INPUT_UNITS] = binary_input

            action_index = _max_index(self._nodes[-_N_OUTPUT_UNITS:])
            self._action = _OUTPUT_INDEX_TO_ACTION[action_index]

ANNStructuredAgent.register()
