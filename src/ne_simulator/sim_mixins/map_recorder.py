# -*- coding: utf-8 -*-
from .base import SimBase


class MapRecorder(SimBase):
    """ Save each map to memory.

    Configuration:
      None

    Access maps to get a list of all recorded maps. Each map consists of lines
    (rows) of Object symbols. For Example:
    [["###", "# #", "###"]]
    """

    def __init__(self, configuration):
        self._maps = []
        super().__init__(configuration)

    @property
    def maps(self):
        return self._maps

    def record_map(self):
        super().record_map()
        self._maps.append(self._map.get_map_lines())
