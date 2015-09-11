# -*- coding: utf-8 -*-
from random import choice, random

from ..position import directions, turn
from .empty import Empty
from .food import Food
from .sim_object import SimObject


def _is_food(obj):
    return isinstance(obj, Food)


def _is_empty(obj):
    return isinstance(obj, Empty)


class RandomAgent(SimObject):
    """ Randomly choose one of the possible actions each turn.

    The agent has a limited life time (100 turns). It can eat food (10 turns
    for each 1 energy point).
    """

    SYMBOL = 'r'

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self._energy = 10.0
        self._direction = choice(directions)
        self._possible_actions = []

    @property
    def direction(self):
        return self._direction

    def set_direction(self, direction):
        super().set_direction(direction)
        self._direction = direction

    def add_energy(self, energy):
        super().add_energy(energy)
        self._energy += energy

    def start_turn(self, objects_map):
        """
        :type objects_map: ObjectsMap
        """
        # Reduce energy.
        self._energy -= 0.1
        if self._energy <= 0.0001:
            actions = [self.Action.DIE]
        else:
            # What is visible to the agent?
            position = objects_map.get_position_for_object(self)

            front = objects_map.get_object_for_position(
                position.move(self._direction))
            left = objects_map.get_object_for_position(
                position.move(turn(self._direction, False)))
            right = objects_map.get_object_for_position(
                position.move(turn(self._direction, True)))

            visible = (front, left, right)

            # What could the agent do?
            actions = [
                self.Action.TURN_LEFT
                if random() >= 0.5 else self.Action.TURN_RIGHT]

            if any(map(_is_food, visible)):
                actions.append(self.Action.EAT)
            if any(map(_is_empty, visible)):
                actions.append(self.Action.MOVE)
        self._possible_actions = actions

    def action(self):
        return choice(self._possible_actions)


RandomAgent.register()
