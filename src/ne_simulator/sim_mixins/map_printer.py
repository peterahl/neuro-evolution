# -*- coding: utf-8 -*-
from inspect import isfunction
from os import rename
from os.path import join
from subprocess import call
from time import sleep

from ne_simulator.sim_objects.neat_agent import NeatAgent


class MapPrinter():
    """ Print each map.

    Configuration:
     - map_printer_delimiter: string to be printed after each map

    If map_printer_delimiter is a function it will be called with self as
    argument and its return value will be printed instead.
    This allows for example to print: "-" * self._width
    """

    def __init__(self, configuration, state, generation_id, simulation_id):
        self._printer_delimiter = configuration.get(
            "map_printer_delimiter", "")
        output_dir = configuration.get("map_printer_output_dir", None)
        if output_dir is not None:
            self._printer_map_file_name = join(
                output_dir, "{}-{}".format(generation_id, simulation_id))
            self._printer_map_file = open(self._printer_map_file_name, "wt")
        super().__init__(configuration, state, generation_id, simulation_id)

    def _map_printer_build_map(self):
        map_string = "\n".join(self._map.get_map_lines())
        delimiter = self._printer_delimiter
        if isfunction(delimiter):
            map_string += "\n" + delimiter(self)
        return map_string

    def record_map(self):
        super().record_map()
        map_string = self._map_printer_build_map()
        if self._printer_map_file is not None:
            self._printer_map_file.write(map_string + "\n")
        else:
            sleep(0.05)
            call(['clear'])
            print(map_string)

    def should_run(self):
        should_run = super().should_run()
        # Close output file.
        if not should_run and self._printer_map_file:
            self._printer_map_file.close()
            self._printer_map_file = None
            # Attach score to filename.
            score = (
                self._state[NeatAgent.CONTEXT_KEY_PREFIX][NeatAgent.SCORE_KEY])
            rename(
                self._printer_map_file_name,
                self._printer_map_file_name + "-{}.txt".format(score))
        return should_run
