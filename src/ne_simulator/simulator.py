# -*- coding: utf-8 -*-
from .objects_map import ObjectsMap
from .position import turn
from .sim_mixins.base import SimBase
from .sim_objects import SimObject, Empty


class Simulator(SimBase):

    def __init__(self, configuration):
        self._map = ObjectsMap(configuration)
        self._step_count = 0
        super().__init__(configuration)

    def should_run(self):
        return False

    def record_map(self):
        pass

    def _move_object(self, o):
        """
        :type o: SimObject
        """
        position = self._map.get_position_for_object(o)
        new_position = position.move(o.direction)
        try:
            other_object = self._map.get_object_for_position(new_position)
        except IndexError:
            other_object = None
        if isinstance(other_object, Empty):
            self._map.set_object(o, new_position)
            self._map.set_object(other_object, position)

    def _turn_object(self, o, action):
        """
        :type o: SimObject
        :type action: SimObject.Action
        """
        o.set_direction(
            turn(o.direction, action == SimObject.Action.TURN_RIGHT))

    def _eat(self, o):
        """
        :type o: SimObject
        """
        other_position = self._map.get_position_for_object(o).move(o.direction)
        other_object = self._map.get_object_for_position(other_position)
        energy = other_object.remove_energy()
        if energy is not None:
            o.add_energy(energy)

    def perform_action(self, o):
        """
        :type o: SimObject
        """
        Action = SimObject.Action  # shortcut
        action = o.action()
        if action == Action.DIE:
            self._map.set_object(Empty(), self._map.get_position_for_object(o))
        if action == Action.MOVE:
            self._move_object(o)
        if action in (Action.TURN_LEFT, Action.TURN_RIGHT):
            self._turn_object(o, action)
        if action == Action.EAT:
            self._eat(o)

    def run(self):
        # TODO: life energy?
        self.record_map()
        while self.should_run():
            for o in self._map:
                o.start_turn(self._map)
            for o in self._map:
                o.wait_until_ready()
            objects = [o for o in self._map]
            for o in objects:
                self.perform_action(o)
            self._step_count += 1
            self.record_map()
