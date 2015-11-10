# -*- coding: utf-8 -*-
"""
Evolution: create children by adding a small random number to non-zero weights.
No crossing between agents.
Scoring: 1 point for changing position, 3 points for eating.
"""
from ne_simulator import SIMULATOR_CONFIGURATION, SIMULATOR_CLASS,\
    CONFIGURATION_MAP
from ne_simulator.maps import food_9x9
from ne_simulator.sim_objects.ann_simple_agent import ANNSimpleAgent
from ne_simulator.sim_objects import Food


EVOLUTION_KWDS = {
    "max_generations": 5000,
    "multiprocessing": True,
}

SIMULATION_COUNTS = 6

SCENARIOS = [
    {
        SIMULATOR_CLASS: [
            "ne_simulator.sim_mixins.UntilNoObjects",
            "ne_simulator.simulator.Simulator"
        ],
        SIMULATOR_CONFIGURATION: {
            CONFIGURATION_MAP: food_9x9,
            "until_no_objects": (ANNSimpleAgent, Food)
        }
    }
]
