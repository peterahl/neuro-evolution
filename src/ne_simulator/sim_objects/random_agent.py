# -*- coding: utf-8 -*-
from random import choice, random

from ..position import directions, turn
from .empty import Empty
from .food import Food
from .sim_object import SimObject


_ADD_RANDOM_WRONG_ACTION = "action_error"

# Initial action probabilities.
_ACTION_PROBABILLITIES = {
    SimObject.Action.EAT: 0.5,
    SimObject.Action.MOVE: 0.5,
    SimObject.Action.TURN_LEFT: 0.5,
    SimObject.Action.TURN_RIGHT: 0.5,
    _ADD_RANDOM_WRONG_ACTION: 0.5,
}

_PROBABILITIES_ORDERING = (
    SimObject.Action.EAT,
    SimObject.Action.MOVE,
    SimObject.Action.TURN_LEFT,
    SimObject.Action.TURN_RIGHT,
    _ADD_RANDOM_WRONG_ACTION,
)

_POSSIBLE_ACTIONS = set([
    SimObject.Action.EAT,
    SimObject.Action.MOVE,
    SimObject.Action.TURN_LEFT,
    SimObject.Action.TURN_RIGHT,
])


def _is_food(obj):
    return getattr(obj, 'SYMBOL', None) == Food.SYMBOL


def _is_empty(obj):
    return getattr(obj, 'SYMBOL', None) == Empty.SYMBOL


def state_to_list(state):
    return [state[p] for p in _PROBABILITIES_ORDERING]


def list_to_state(probabilities):
    return {k: v for k, v in zip(_PROBABILITIES_ORDERING, probabilities)}


class RandomAgent(SimObject):
    """ Randomly choose one of the possible actions each turn.

    The agent has a limited life time (100 turns). It can eat food (10 turns
    for each 1 energy point).

    The score is measured in move actions plus eat actions.
    """

    SYMBOL = 'r'

    STATE_KEY = "random_agent"

    SCORE_KEY = "score"

    def __init__(self, state, *args, **kwds):
        super().__init__(state, *args, **kwds)
        self._state = state
        self._energy = 10.0
        self._direction = choice(directions)
        self._possible_actions = []
        agent_state = self._state.get(self.STATE_KEY)
        if agent_state is None:
            agent_state = {
                k: v + random() * 0.3 - 0.15
                for k, v in _ACTION_PROBABILLITIES.items()
            }
        self._probabilities = agent_state
        self._state[self.STATE_KEY] = self._probabilities
        self._state[self.SCORE_KEY] = 0
        self._last_position = None

    @property
    def direction(self):
        return self._direction

    def set_direction(self, direction):
        super().set_direction(direction)
        self._direction = direction

    def add_energy(self, energy):
        super().add_energy(energy)
        self._energy += energy
        self._state[self.SCORE_KEY] += 1

    def start_turn(self, objects_map):
        """
        :type objects_map: ObjectsMap
        """
        # Reduce energy.
        self._energy -= 0.1
        if self._energy <= 0.0001:
            actions = [self.Action.DIE]
        else:
            # Get action, improve and set score.
            position = objects_map.get_position_for_object(self)
            if (self._last_position is not None and
                    position != self._last_position):
                self._state[self.SCORE_KEY] += 1
            self._last_position = position

            # What is visible to the agent?
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

            # Make probability check for each action.
            actions = [
                a for a in actions if random() < _ACTION_PROBABILLITIES[a]]

            # Add random impossible action.
            if random() < self._probabilities[_ADD_RANDOM_WRONG_ACTION]:
                wrong_actions = _POSSIBLE_ACTIONS - set(actions)
                if wrong_actions:
                    actions.append(choice(list(wrong_actions)))
        self._possible_actions = actions

    def action(self):
        if self._possible_actions:
            return choice(self._possible_actions)
        return None


RandomAgent.register()
