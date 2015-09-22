# -*- coding: utf-8 -*-
from inspect import isfunction
from subprocess import call
from .base import SimBase
from time import sleep

class MapPrinter(SimBase):
    """ Print each map.

    Configuration:
     - map_printer_delimiter: string to be printed after each map

    If map_printer_delimiter is a function it will be called with self as
    argument and its return value will be printed instead.
    This allows for example to print: "-" * self._width
    """

    def __init__(self, configuration):
        super().__init__(configuration)
        self._printer_delimiter = configuration.get(
            "map_printer_delimiter", "")

    def record_map(self):
        super().record_map()
        sleep(0.05)
        call(['clear'])
        print("\n".join(self._map.get_map_lines()))
        delimiter = self._printer_delimiter
        if isfunction(delimiter):
            delimiter = delimiter(self)
        print(delimiter)