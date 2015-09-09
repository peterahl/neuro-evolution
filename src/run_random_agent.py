#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ne_simulator.sim_mixins.map_printer import MapPrinter
from ne_simulator.simulator import Simulator
from ne_simulator.sim_mixins import UntilNoObjects
from ne_simulator.sim_objects.random_agent import RandomAgent


def _print_step_count(sim):
    """
    :type sim: Simulator
    """
    return "-" * sim._map._width + "\n" + "Step: {}\n".format(sim._step_count)


def main():
    class Sim(UntilNoObjects, MapPrinter, Simulator):
        pass

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
        "until_no_objects": (RandomAgent),
        "map_printer_delimiter": _print_step_count,
    }
    Sim(configuration).run()

if __name__ == '__main__':
    main()
