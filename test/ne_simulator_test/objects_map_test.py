# -*- coding: utf-8 -*-
from unittest.case import TestCase

from ne_simulator.objects_map import ObjectsMap, MapDimensionMissMatch


class ObjectsMapTest(TestCase):

    def test_map_representation(self):
        """ Create map with walls and empty spaces and check get_map_lines. """
        map_lines = [
            "######",
            "#    #",
            "#  # #",
            "#  # #",
            "######"
        ]
        objects_map = ObjectsMap({"map": map_lines})
        self.assertEqual(map_lines, objects_map.get_map_lines())

    def test_bad_map_representation(self):
        """ Create a map where not all rows have the same length and check if
        reading the map fails. """
        with self.assertRaises(MapDimensionMissMatch):
            ObjectsMap({"map": ["######", "##"]})
