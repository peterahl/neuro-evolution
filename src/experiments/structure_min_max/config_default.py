# -*- coding: utf-8 -*-
""" Run the agent once without evolution and show the labyrinth.

Press enter to continue.
"""
from ne_simulator import SIMULATOR_CONFIGURATION, SIMULATOR_CLASS,\
    CONFIGURATION_MAP
from ne_simulator.maps import food_9x9
from ne_simulator.sim_objects.ann_structure_agent import \
    ANNStructuredAgent  # @UnusedImport register the Agent
# from ne_simulator.objects_map import CONFIGURATION_PARAMETERS
# from ne_simulator.sim_objects.sim_agent import SCORE_MONITOR


def _print_step_count(sim):
    """
    :type sim: ne_simulator.Simulator
    """
    return "-" * sim._map._width + "\n" + "Step: {}\n".format(sim._step_count)


SCENARIOS = [
    {
        SIMULATOR_CLASS: [
            "ne_simulator.sim_mixins.StepsLimiter",
            "ne_simulator.sim_mixins.MapPrinter",
            "ne_simulator.Simulator"
        ],
        SIMULATOR_CONFIGURATION: {
            CONFIGURATION_MAP: food_9x9,
            "steps_limiter_steps": 50,
            "map_printer_delimiter": _print_step_count
        }
    }
]
