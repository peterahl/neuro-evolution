# -*- coding: utf-8 -*-
from unittest.case import TestCase

from ne_simulator.sim_mixins import UntilNoObjects
from ne_simulator.sim_objects.random_agent import RandomAgent
from ne_simulator.simulator import Simulator


class _Sim(UntilNoObjects, Simulator):
    pass


class RandomAgentTest(TestCase):

    def setUp(self):
        super().setUp()
        # Normally random agent is not register on start up.
        # Unregister (if necessary) and register it now, and undo that at tear
        # down.
        RandomAgent.deregister()
        RandomAgent.register()

    def tearDown(self):
        RandomAgent.deregister()
        super().tearDown()

    def test_run_random_agent(self):
        """ Let a random agent run loose and see if it survives at least as
        long as the initial energy suffices.
        """
        configuration = {
            "map": [
                "#########",
                "#++     #",
                "#       #",
                "# r  ####",
                "#    ++ #",
                "#       #",
                "##     +#",
                "#+      #",
                "#########",
            ],
            "until_no_objects": RandomAgent,
        }
        sim = _Sim(configuration, {})
        sim.run()
        self.assertGreaterEqual(sim._step_count, 100)
