# -*- coding: utf-8 -*-
from itertools import chain

from .position import Position
from .sim_objects.sim_object import SimObject


class MapDimensionMissMatch(Exception):
    pass


class ObjectsMap():

    def __init__(self, configuration):
        """
        {
          map: ["######", "#  # #", "#  # #", "######"],
          parameters: {(0, 0): (["argument"], {"key": "value"})}
        }
        """
        objects_map = configuration["map"]  # shortcut
        params = configuration.get("parameters", {})  # shortcut
        self._map = list(chain.from_iterable(
            [SimObject.from_symbol(symbol, params.get((x, y)))
                for x, symbol in enumerate(row)]
            for y, row in enumerate(objects_map)))
        self._height = len(objects_map)
        self._width = len(objects_map[0])
        if self._height * self._width != len(self._map):
            raise MapDimensionMissMatch(
                (self._height * self._width, len(self._map)))
        self._positions = {
            o: self._position_for_index(i) for i, o in enumerate(self._map)}

    def __iter__(self):
        return iter(self._map)

    def _position_for_index(self, i):
        return Position(i % self._width, i // self._width)

    def _index_for_position(self, p):
        index = p.y * self._width + p.x
        if index < 0 or index >= self._width * self._height:
            raise IndexError(index)
        return index

    def get_map_lines(self):
        return [
            "".join(
                o.symbol
                for o in self._map[offset: offset + self._width])
            for offset in range(0, self._height * self._width, self._width)]

    def get_position_for_object(self, o):
        """
        :rtype: Position
        """
        return self._positions[o]

    def get_object_for_position(self, p):
        """
        :rtype: SimObject
        """
        return self._map[self._index_for_position(p)]

    def set_object(self, o, p):
        self._map[self._index_for_position(p)] = o
        self._positions[o] = p
