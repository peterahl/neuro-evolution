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
    structure = [
        [(randint(_INITIAL_MIN_NODES, _INITIAL_MAX_NODES), {})
            for _ in range(randint(_INITIAL_LAYERS_MIN, _INITIAL_LAYERS_MAX))]
        for _ in range(_INITIAL_UNITS)
    ]
    for j, unit in enumerate(structure):
        for i, (_, conns) in enumerate(unit):
            others = [n for n in range(len(unit)) if n != i]
            for o in others:
                conns[o] = (
                    _rand_range(_INITIAL_MU_RANGE), _INITIAL_SIGMA,
                    randint(_INITIAL_OUTDEGREE_MIN, _INITIAL_OUTDEGREE_MAX))
            if i == len(unit) - 1 and j < len(structure) - 1:
                others = [n for n in range(len(structure)) if n != j]
                print(others)
                conns[None] = {
                    n: (_rand_range(_INITIAL_MU_RANGE), _INITIAL_SIGMA,
                        randint(
                            _INITIAL_OUTDEGREE_MIN, _INITIAL_OUTDEGREE_MAX))
                    for n in others}
    return structure


class ANNStructuredAgent(SimAgent):

    STRUCTURE_KEY = 'structure'

    def __init__(self, context, *args, **kwds):
        super().__init__(context, *args, **kwds)
        structure = self._ctx.get(self.STRUCTURE_KEY)
        if structure is None:
            structure = _create_initial_structure()

ANNStructuredAgent.register()
