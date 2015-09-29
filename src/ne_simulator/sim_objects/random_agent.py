# -*- coding: utf-8 -*-
from random import choice, random

from ..position import directions
from .empty import Empty
from .food import Food
from .sim_object import SimObject
from .sim_agent import SimAgent


# Initial action probabilities.
_ACTION_PROBABILLITIES = {
    SimObject.Action.EAT: 0.5,
    SimObject.Action.MOVE: 0.5,
    SimObject.Action.TURN_LEFT: 0.5,
    SimObject.Action.TURN_RIGHT: 0.5,
    SimObject.Action.DO_NOTHING: 0.5,
}

_PROBABILITIES_ORDERING = (
    SimObject.Action.EAT,
    SimObject.Action.MOVE,
    SimObject.Action.TURN_LEFT,
    SimObject.Action.TURN_RIGHT,
    SimObject.Action.DO_NOTHING,
)

_POSSIBLE_ACTIONS = set([
    SimObject.Action.EAT,
    SimObject.Action.MOVE,
    SimObject.Action.TURN_LEFT,
    SimObject.Action.TURN_RIGHT,
])


def _probs_from_context(ctx_probabilities):
    """ Convert context probabilities into agent probabilities.

    :param ctx_probabilities: containing the actual values not Action objects.
    :type state: [float]
    :return: probabilities index with Action
    :rtype: {SimObject.Action: float}
    """
    action_probabilities = zip(_PROBABILITIES_ORDERING, ctx_probabilities)
    return {
        action: probability
        for action, probability in action_probabilities}


def _probs_to_context(probabilities):
    """ Convert agent probabilities into context probabilities.

    :param probabilities: {SimObject.Action: float}
    :return: ordered probabilities as list
    :rtype: [float]
    """
    return [probabilities[action] for action in _PROBABILITIES_ORDERING]


class RandomAgent(SimAgent):
    """ Randomly choose one of the possible actions each turn.

    The agent has a limited life time (100 turns). It can eat food (10 turns
    for each 1 energy point).

    The score is measured in move actions plus eat actions.
    """

    PROBABILITIES_KEY = "probabilities"

    def __init__(self, state, *args, **kwds):
        super().__init__(state, *args, **kwds)
        self._energy = 10.0
        self._monitor['_direction'] = choice(directions)
        probabilities = self._ctx.get(self.PROBABILITIES_KEY)
        if probabilities is None:
            probabilities = {
                k: v + random() * 0.3 - 0.15
                for k, v in _ACTION_PROBABILLITIES.items()
            }
            # Set the state, taking care to save values not Action objects!
            self._ctx[self.PROBABILITIES_KEY] = _probs_to_context(
                probabilities)
        else:
            probabilities = _probs_from_context(probabilities)
        self._probabilities = probabilities

    def start_turn(self, objects_map):
        """
        :type objects_map: ObjectsMap
        """
        super().start_turn(objects_map)
        # Reduce energy.
        self._energy -= 0.1
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
