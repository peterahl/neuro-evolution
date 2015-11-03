# -*- coding: utf-8 -*-
"""
Evolution: create children by adding a small random number to non-zero weights.
No crossing between agents.
Scoring: 1 point for changing position, 3 points for eating.
"""
from ne_simulator import SIMULATOR_CONFIGURATION, SIMULATOR_CLASS,\
    CONFIGURATION_MAP
from ne_simulator.maps import food_9x9
# from ne_simulator import CONFIGURATION_PARAMETERS
# from ne_simulator import SCORE_MONITOR


# EVOLUTION = "default"

EVOLUTION_KWDS = {
    "max_generations": 2
}

SIMULATION_COUNTS = 6

SCENARIOS = [
    {
        SIMULATOR_CLASS: [
            "ne_simulator.sim_mixins.steps_limiter.StepsLimiter",
            "ne_simulator.simulator.Simulator"
        ],
        # SCORE_MONITOR: "default",
        SIMULATOR_CONFIGURATION: {
            CONFIGURATION_MAP: food_9x9,
            # CONFIGURATION_PARAMETERS: {
            # },
            "steps_limiter_steps": 10
        }
    }
]
