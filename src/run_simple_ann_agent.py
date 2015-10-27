#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from ne_simulator.sim_mixins import StepsLimiter
from ne_simulator.sim_mixins.map_printer import MapPrinter
from ne_simulator.sim_objects.ann_simple_agent import \
    ANNSimpleAgent  # @UnusedImport
from ne_simulator.simulator import Simulator


def _print_step_count(sim):
    """
    :type sim: Simulator
    """
    return "-" * sim._map._width + "\n" + "Step: {}\n".format(sim._step_count)


def main():
    class Sim(StepsLimiter, MapPrinter, Simulator):
        pass

    with open('configurations/minimap.json') as jfile:
        configuration = json.load(jfile)

    configuration["map_printer_delimiter"] = _print_step_count
    configuration["steps_limiter_steps"] = 200
    configuration["parameters"] = {(2, 3): ([], {})}
    Sim(configuration, {}).run()

if __name__ == '__main__':
    main()
