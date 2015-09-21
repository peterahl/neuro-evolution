# -*- coding: utf-8 -*-
from unittest.case import TestCase

from ne_simulator.position import Direction
from ne_simulator.sim_objects import SimObject
from ne_simulator_test.utils import RecorderSimulator


class _ActionAgent(SimObject):
    """ Direction aware test agent that performs the given actions. """

    def __init__(self, state, direction, actions, *args, **kwds):
        super().__init__(state, *args, **kwds)
        self._direction = direction
        self._actions = actions

    @property
    def direction(self):
        return self._direction

    def set_direction(self, direction):
        super().set_direction(direction)
        self._direction = direction

    def action(self):
        return self._actions.pop()


class ActionTurnTest(TestCase):

    def setUp(self):
        super().setUp()
        _ActionAgent.register()

    def tearDown(self):
        _ActionAgent.deregister()
        super().tearDown()

    def test_turn(self):
        """ Place a test agent and turn left, move, then turn right and move
        again. Check the map after each turn.
        """
        Action = SimObject.Action  # shortcut
        actions = [
            Action.MOVE, Action.TURN_RIGHT, Action.MOVE, Action.TURN_LEFT]
        map_lines = ["  ", " T"]
        configuration = {
            "map": map_lines,
            "parameters": {(1, 1): ([Direction.NORTH, actions], {})},
            "steps_limiter_steps": 4
        }
        sim = RecorderSimulator(configuration, {})
        sim.run()
        self.assertEqual(
            sim.maps,
            [map_lines, ["  ", " T"], ["  ", "T "], ["  ", "T "],
                ["T ", "  "]])
