# -*- coding: utf-8 -*-
from itertools import chain

from .position import Position
from .sim_objects.sim_object import SimObject


class MapDimensionMismatch(Exception):
    pass


class ObjectsMap():

    def __init__(self, configuration, state):
        """
        {
          # ASCII representation of map as array of strings
          map: ["######", "#  # #", "#  # #", "######"],

          # tuple of *args, **kwds
          parameters: {(0, 0): (["argument"], {"key": "value"})}

        }
        """
        objects_map = configuration["map"]  # shortcut
        params = configuration.get("parameters", {})  # shortcut

        # Create internal map representation containing objects at their
        # respective (x,y) positions
        self._map = list(
            chain.from_iterable(
                [
                    SimObject.from_symbol(symbol, state, params.get((x, y)))
                    for x, symbol in enumerate(row)
                ]
                for y, row in enumerate(objects_map)
            )
        )

        # Save dimensions of map
        self._height = len(objects_map)
        self._width = len(objects_map[0])

        # sanity check for map
        if self._height * self._width != len(self._map):
            raise MapDimensionMismatch(
                (self._height * self._width, len(self._map)))

        # Create lookup dictionary (hash table) for objects
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
