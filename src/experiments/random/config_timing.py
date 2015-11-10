# -*- coding: utf-8 -*-
""" For timing and optimization purposes.
"""
from ne_simulator import SIMULATOR_CONFIGURATION, SIMULATOR_CLASS,\
    CONFIGURATION_MAP
from ne_simulator.maps import food_9x9
from ne_simulator.sim_objects.random_agent import RandomAgent  # @UnusedImport


# Started with 180/16 (user/sys)
# Improved sim loop 120/12 (user/sys)


EVOLUTION_KWDS = {
    "wait_for_enter": False,
    "multiprocessing": False,
}

SCENARIOS = [
    {
        SIMULATOR_CLASS: [
            "ne_simulator.sim_mixins.StepsLimiter",
            "ne_simulator.Simulator"
        ],
        SIMULATOR_CONFIGURATION: {
            CONFIGURATION_MAP: food_9x9,
            "steps_limiter_steps": 100,
        }
    }
]
