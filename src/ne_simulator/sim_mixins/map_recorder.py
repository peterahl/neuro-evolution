# -*- coding: utf-8 -*-


class MapRecorder():
    """ Save each map to memory.

    Configuration:
      None

    Access maps to get a list of all recorded maps. Each map consists of lines
    (rows) of Object symbols. For Example:
    [["###", "# #", "###"]]
    """

    def __init__(self, configuration, state):
        self._maps = []
        super().__init__(configuration, state)

    @property
    def maps(self):
        return self._maps

    def record_map(self):
        super().record_map()
        self._maps.append(self._map.get_map_lines())
