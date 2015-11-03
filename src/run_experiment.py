#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from importlib import import_module

from ne_simulator.import_util import import_obj
from ne_simulator.evolution import SIMULATOR_CONFIGURATION, SIMULATOR_CLASS
from ne_simulator.objects_map import ObjectsMap, CONFIGURATION_PARAMETERS
from ne_simulator.sim_objects.sim_agent import SCORE_MONITOR_PARAMETER,\
    SCORE_MONITOR


_EXPERIMENTS_PACKAGE = "experiments"

_CONFIG_PREFIX = "config_"

_SIMULATION_COUNTS_VARIABLE = "SIMULATION_COUNTS"

_SCENARIOS_VARIABLE = "SCENARIOS"

_EVOLUTION_CONFIG = "EVOLUTION"

_EVOLUTION_KWDS_CONFIG = "EVOLUTION_KWDS"

_EVOLUTION_DEFAULT = "default"

_EVOLUTION_PREFIX = "evolution_"

_MONITOR_DEFAULT = "default"

_MONITOR_PREFIX = "monitor_"


def _build_class(class_name, classes):
    """ Import all classes from the parameter and then build a new class with
    the given name.

    :param class_name: the name for the new class
    :param classes: one ore more Classes to build the new class out of
    """
    if not isinstance(classes, (list, tuple)):
        classes = (classes, )
    return type(class_name, tuple(import_obj(c) for c in classes), {})


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "experiment",
        help="Name of the experiment. The runner will look for it in "
        "src/experiments.")
    parser.add_argument(
        "-c", "--configuration", type=str, default="default",
        help="Specify the configuration to be used. It must exist as a "
        "config_*** import within the experiment! Defaults to 'default'.")
    args = parser.parse_args()
    experiment = args.experiment
    # TODO: add configuration to argument parser above.
    configuration = args.configuration
    # Import experiment package.
    experiment = import_module(_EXPERIMENTS_PACKAGE + "." + experiment)
    # TODO: use logging.
    if experiment.__doc__:
        print(experiment.__doc__[1:])
    configuration = getattr(experiment, _CONFIG_PREFIX + configuration)
    if configuration.__doc__:
        print(configuration.__doc__[1:])
    # Build and import simulation and monitor classes.
    scenarios = getattr(configuration, _SCENARIOS_VARIABLE)
    for scenario in scenarios:
        sim_config = scenario[SIMULATOR_CONFIGURATION]  # shortcut
        scenario[SIMULATOR_CLASS] = _build_class(
            "Simulator", scenario[SIMULATOR_CLASS])
        monitor_module = getattr(
            experiment,
            _MONITOR_PREFIX +
            scenario.get(SCORE_MONITOR, _MONITOR_DEFAULT))
        # Add score monitor parameter to all map objects.
        map_lines = ObjectsMap.get_map(sim_config)
        height = len(map_lines)
        width = len(map_lines[0])
        params = sim_config.get(CONFIGURATION_PARAMETERS, {})
        for x in range(width):
            for y in range(height):
                args, kwds = params.get((x, y), ((), {}))
                kwds[SCORE_MONITOR_PARAMETER] = monitor_module.Monitor
                params[(x, y)] = (args, kwds)
        sim_config[CONFIGURATION_PARAMETERS] = params
    # Get evolution class, create insance and run!
    evolution = getattr(configuration, _EVOLUTION_CONFIG, _EVOLUTION_DEFAULT)
    evolution = getattr(experiment, _EVOLUTION_PREFIX + evolution).Evolution(
        scenarios, getattr(configuration, _SIMULATION_COUNTS_VARIABLE, 1),
        **getattr(configuration, _EVOLUTION_KWDS_CONFIG, {}))
    evolution.run()

if __name__ == '__main__':
    main()
