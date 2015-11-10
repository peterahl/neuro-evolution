# -*- coding: utf-8 -*-
""" Run the agent once without evolution and show the labyrinth.

Press enter to continue.
"""
from ne_simulator import SIMULATOR_CONFIGURATION, SIMULATOR_CLASS,\
    CONFIGURATION_MAP
from ne_simulator.maps import food_9x9
from ne_simulator.sim_objects.random_agent import RandomAgent
# from ne_simulator.objects_map import CONFIGURATION_PARAMETERS
# from ne_simulator.sim_objects.sim_agent import SCORE_MONITOR


def _print_step_count(sim):
    """
    :type sim: ne_simulator.Simulator
    """
    return "-" * sim._map._width + "\n" + "Step: {}\n".format(sim._step_count)


# EVOLUTION = "default"

EVOLUTION_KWDS = {
    "wait_for_enter": True
}

# SIMULATION_COUNTS = 1

SCENARIOS = [
    {
        SIMULATOR_CLASS: [
            "ne_simulator.sim_mixins.UntilNoObjects",
            "ne_simulator.sim_mixins.MapPrinter",
            "ne_simulator.Simulator"
        ],
        # SCORE_MONITOR: "default",
        SIMULATOR_CONFIGURATION: {
            CONFIGURATION_MAP: food_9x9,
            # CONFIGURATION_PARAMETERS: {
            # },
            "until_no_objects": (RandomAgent),
            "map_printer_delimiter": _print_step_count
        }
    }
]
