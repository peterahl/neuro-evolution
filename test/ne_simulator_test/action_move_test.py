# -*- coding: utf-8 -*-
from unittest.case import TestCase

from ne_simulator.position import Direction
from ne_simulator.sim_objects import SimObject
from ne_simulator_test.utils import RecorderSimulator


class _MoveAgent(SimObject):
    """ Test agent that moves in the given directions. """

    _instance = None

    def __init__(self, state, directions, *args, **kwds):
        super().__init__(state, *args, **kwds)
        _MoveAgent._instance = self
        self._directions = directions
        self._direction = None
        self.move_agend_actions_count = 0

    @property
    def direction(self):
        return self._direction

    def action(self):
        self.move_agend_actions_count += 1
        self._direction = self._directions.pop()
        return self.Action.MOVE


class _ActionAgent(SimObject):
    """ Direction aware test agent that performs the given actions. """

    def __init__(self, direction, actions, *args, **kwds):
        super().__init__(*args, **kwds)
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


class _MapContainer():

    MAP = None


class ActionMoveTest(TestCase):

    def setUp(self):
        super().setUp()
        _MoveAgent.register()

    def tearDown(self):
        _MoveAgent.deregister()
        super().tearDown()

    def test_move_outside_map(self):
        """ Place test agent on border and run one move action, see that
        nothing (no move) happens.
        """
        _MapContainer.MAP = "T"
        configuration = {
            "map": _MapContainer,
            "parameters": {(0, 0): ([[Direction.NORTH]], {})},
            "steps_limiter_steps": 1
        }
        sim = RecorderSimulator(configuration, {})
        sim.run()
        agent = _MoveAgent._instance
        self.assertIsNotNone(agent)
        self.assertEqual(agent.move_agend_actions_count, 1)
        self.assertEqual(
            sim._map.get_map_lines(), _MapContainer.MAP.split("\n"))

    def test_move(self):
        """ Place a test agent and move towards NORTH, EAST, SOUTH, WEST and
        check the map after each run.
        """
        nesw = [
            Direction.WEST, Direction.SOUTH, Direction.EAST, Direction.NORTH]
        map_lines = ["  ", "T "]
        _MapContainer.MAP = "\n".join(map_lines)
        configuration = {
            "map": _MapContainer,
            "parameters": {(0, 1): ([nesw], {})},
            "steps_limiter_steps": 4
        }
        sim = RecorderSimulator(configuration, {})
        sim.run()
        self.assertEqual(
            sim.maps,
            [map_lines, ["T ", "  "], [" T", "  "], ["  ", " T"],
                map_lines])
