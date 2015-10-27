# -*- coding: utf-8 -*-
from random import randint, random

from .sim_agent import SimAgent


# _OBJECT_TO_INPUT = {
#     Wall.SYMBOL: (1, 0, 0), Empty.SYMBOL: (0, 1, 0), Food.SYMBOL: (0, 0, 1)}
#
# _MAX_ENERGY = 1.0
#
# _ENERGY_LEVELS = 5
#
# # Fields front, left, right, energy level and last action ok
# _NUMBER_OF_INPUTS = len(_OBJECT_TO_INPUT) * 3 + _ENERGY_LEVELS
#
# _OUTPUT_INDEX_TO_ACTION = {
#     0: SimObject.Action.MOVE,
#     1: SimObject.Action.EAT,
#     2: SimObject.Action.TURN_LEFT,
#     3: SimObject.Action.TURN_RIGHT,
#     4: SimObject.Action.DO_NOTHING
# }

_INITIAL_UNITS = 2

_INITIAL_MIN_NODES = 4

_INITIAL_MAX_NODES = 8

_INITIAL_LAYERS_MIN = 4

_INITIAL_LAYERS_MAX = 6

_INITIAL_MU_RANGE = 0.5

_INITIAL_SIGMA = 0.3

_INITIAL_OUTDEGREE_MIN = 0

_INITIAL_OUTDEGREE_MAX = 7


def _rand_range(rng):
    return random() * 2 * rng - rng


def _create_initial_structure():
    """Create the inital randomized structure for the agent.

    For the structure, see the ANNStructuredAgent configuration below.

    """
    # Create units (populations or columns) and layers with their nodes count.
    structure = [
        [(randint(_INITIAL_MIN_NODES, _INITIAL_MAX_NODES), {})
            for _ in range(randint(_INITIAL_LAYERS_MIN, _INITIAL_LAYERS_MAX))]
        for _ in range(_INITIAL_UNITS)
    ]
    # For each layer in each unit: add the configuration (connections).
    for j, unit in enumerate(structure):
        for i, (_, conns) in enumerate(unit):
            # Connect this layer to other layers in the same unit.
            others = [n for n in range(len(unit)) if n != i]
            for o in others:
                conns[o] = (
                    _rand_range(_INITIAL_MU_RANGE), _INITIAL_SIGMA,
                    randint(_INITIAL_OUTDEGREE_MIN, _INITIAL_OUTDEGREE_MAX))
            # Connect the last layer of the current unit to other units.
            if i == len(unit) - 1 and j < len(structure) - 1:
                others = [n for n in range(len(structure)) if n != j]
                conns[None] = {
                    n: (_rand_range(_INITIAL_MU_RANGE), _INITIAL_SIGMA,
                        randint(
                            _INITIAL_OUTDEGREE_MIN, _INITIAL_OUTDEGREE_MAX))
                    for n in others}
    # TODO: set nodes count for global input and output manually.
    return structure


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

    STRUCTURE_KEY = "structure"

    def __init__(self, context, *args, **kwds):
        super().__init__(context, *args, **kwds)
        # Get or set the structure.
        structure = self._ctx.get(self.STRUCTURE_KEY)
        if structure is None:
            structure = _create_initial_structure()
            self._ctx[self.STRUCTURE_KEY] = structure
        # TODO: generate weights.


ANNStructuredAgent.register()
