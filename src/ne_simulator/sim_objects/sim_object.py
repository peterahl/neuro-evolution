# -*- coding: utf-8 -*-
from enum import Enum, unique


class DuplicateSymbol(Exception):
    pass


class SimObject():

    _objects = {}

    SYMBOL = "T"  # reserved for testing!

    def __init__(self, state, *args, **kwds):
        """ Placeholder.

        Use state to get parameters (previous simulation state) for the object.

        :type state: dict
        """
        super().__init__()

    @unique
    class Action(Enum):

        DIE = 0

        MOVE = 1

        TURN_LEFT = 2

        TURN_RIGHT = 3

        EAT = 4

        DO_NOTHING = None

    @property
    def symbol(self):
        return self.SYMBOL

    @property
    def direction(self):
        return None

    def add_energy(self, energy):
        """
        :type energy: float
        """
        pass

    def remove_energy(self):
        """
        :rtype: float
        """
        return None

    def set_direction(self, direction):
        """
        :type direction: Direction
        """
        pass

    def start_turn(self, objects_map):
        """
        :type objects_map: ObjectsMap
        """
        pass

    def action(self):
        """ Simulation moves one tick forward, perform action and read inputs
        for next action.

        Do not forget to update the simulation state, if necessary!
        """
        return None

    @classmethod
    def is_me(cls, obj):
        return getattr(obj, 'SYMBOL', None) == cls.SYMBOL

    @classmethod
    def register(cls):
        if cls.SYMBOL in SimObject._objects:
            raise DuplicateSymbol(cls.SYMBOL)
        if cls.SYMBOL is None:
            raise AttributeError(
                'SYMBOL not specified for class {}'.format(cls))
        SimObject._objects[cls.SYMBOL] = cls

    @classmethod
    def deregister(cls):
        SimObject._objects.pop(cls.SYMBOL, None)

    @staticmethod
    def from_symbol(symbol, state, params=None):
        args = []
        kwds = {}
        if params is not None:
            args, kwds = params
        return SimObject._objects[symbol](state, *args, **kwds)
