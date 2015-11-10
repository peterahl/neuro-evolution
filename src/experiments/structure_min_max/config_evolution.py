# -*- coding: utf-8 -*-
""" Let 6 random agents evolve for 10 generations.

Uses multiprocessing.
"""
from ne_simulator import Food, SIMULATOR_CONFIGURATION, SIMULATOR_CLASS, \
    CONFIGURATION_MAP, SCORE_MONITOR
from ne_simulator.maps import food_9x9
from ne_simulator.sim_objects.random_agent import RandomAgent


EVOLUTION = "combine_and_randomize"

EVOLUTION_KWDS = {
    "multiprocessing": True
}

SIMULATION_COUNTS = 6

SCENARIOS = [
    {
        SIMULATOR_CLASS: [
            "ne_simulator.sim_mixins.UntilNoObjects",
            "ne_simulator.Simulator"
        ],
        SCORE_MONITOR: "move_and_eat",
        SIMULATOR_CONFIGURATION: {
            CONFIGURATION_MAP: food_9x9,
            # CONFIGURATION_PARAMETERS: {
            # },
            "until_no_objects": (RandomAgent, Food),
        }
    }
]
