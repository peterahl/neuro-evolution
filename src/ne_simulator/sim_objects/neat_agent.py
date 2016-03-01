# -*- coding: utf-8 -*-
from random import choice, random, randrange

from ..position import Direction
from .empty import Empty
from .food import Food
from .sim_object import SimObject
from .sim_agent import SimAgent

_INPUT_NUMBER = 24
_OUTPUT_NUMBER = 5


class NeatAgent(SimAgent):
    """ Fill in later
    """

    CONNECTIONS_KEY = "connections"

    def __init__(self, state, *args, **kwds):
        super().__init__(state, *args, **kwds)
        self._energy = 10.0
        self._monitor['_direction'] = Direction.NORTH
        self._hidden = 0
        nodes = [i for i in range(_INPUT_NUMBER+_OUTPUT_NUMBER+self._hidden)]
        self._connections = []

        for _ in range(_INPUT_NUMBER):
            self._connections.append(
                [(randrange(_INPUT_NUMBER, len(nodes), 1), randrange(-1, 1))])

        for _ in range(_OUTPUT_NUMBER):
            self._connections.append([])

    def _integrate_network(self,input_state):
        # Paused here
        


    def start_turn(self, objects_map):
        """
        :type objects_map: ObjectsMap
        """
        super().start_turn(objects_map)
        # Reduce energy.
        self._energy -= 0.1  # do not tell the monitor
        if self._energy <= 0.0001:
            actions = [self.Action.DIE]
        else:
            visible = self.get_visible(objects_map)

            # What could the agent do? Nothing or turn are always possible.
            actions = [
                self.Action.DO_NOTHING,
                self.Action.TURN_LEFT
                if random() >= 0.5 else self.Action.TURN_RIGHT]

            if any(map(Food.is_me, visible)):
                actions.append(self.Action.EAT)
            if any(map(Empty.is_me, visible)):
                actions.append(self.Action.MOVE)

            # Make probability check for each action.
            actions = [
                a for a in actions if random() < self._probabilities[a]]
        # Choose what to do.
        self._action = choice(actions) if actions else self.Action.DO_NOTHING

RandomAgent.register()
