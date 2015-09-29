# -*- coding: utf-8 -*-
from unittest.case import TestCase

from ne_simulator.position import Direction
from ne_simulator.sim_objects import SimObject
from ne_simulator_test.utils import RecorderSimulator


class _EatAgent(SimObject):
    """ Test agent with energy level, always eats facing NORTH. """

    _instance = None

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        _EatAgent._instance = self
        self.energy = 0

    @property
    def direction(self):
        return Direction.NORTH

    def add_energy(self, energy):
        super().add_energy(energy)
        self.energy += energy

    def action(self):
        return self.Action.EAT


class ActionTurnTest(TestCase):

    def setUp(self):
        super().setUp()
        _EatAgent.register()

    def tearDown(self):
        _EatAgent.deregister()
        super().tearDown()

    def test_eat(self):
        """ Try to eat one food, check that the energy has been transfered and
        that the food is removed from the map.
        """
        configuration = {
            "map": ["+", "T"],
            "steps_limiter_steps": 2
        }
        sim = RecorderSimulator(configuration, {})
        agent = _EatAgent._instance
        sim.run()
        self.assertAlmostEqual(agent.energy, 1.0, delta=0.0001)
        self.assertEqual(sim.maps[-1], [" ", "T"])
