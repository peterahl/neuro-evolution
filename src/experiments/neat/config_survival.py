# -*- coding: utf-8 -*-
"""
"""
from ne_simulator import SIMULATOR_CONFIGURATION, SIMULATOR_CLASS, \
    CONFIGURATION_MAP
from ne_simulator.maps import food_9x9
from ne_simulator.sim_objects.neat_agent import NeatAgent
from ne_simulator.sim_objects.sim_agent import SCORE_MONITOR


# from ne_simulator.objects_map import CONFIGURATION_PARAMETERS
# from ne_simulator.sim_objects.sim_agent import SCORE_MONITOR
EVOLUTION = "survival"

EVOLUTION_KWDS = {
}

SIMULATION_COUNTS = 20

SCENARIOS = [
    {
        SIMULATOR_CLASS: [
            "ne_simulator.sim_mixins.MapPrinter",
            "ne_simulator.sim_mixins.UntilNoObjects",
            "ne_simulator.Simulator"
        ],
        SCORE_MONITOR: "survival",
        SIMULATOR_CONFIGURATION: {
            CONFIGURATION_MAP: food_9x9,
            # CONFIGURATION_PARAMETERS: {
            # },
            "until_no_objects": (NeatAgent),
            "map_printer_output_dir": "./out",
            "map_printer_delimiter": lambda x: "-"
        }
    }
]
