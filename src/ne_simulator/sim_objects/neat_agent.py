# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import chain
from enum import Enum
from random import random, choice, randrange

from ..position import Direction, turn
from .empty import Empty
from .food import Food
from .sim_agent import SimAgent
from .sim_object import SimObject
from .wall import Wall


_INPUT_NUMBER = 3 * 5 + 4 + 5  # 24, fields, direction, energy

_OUTPUT_NUMBER = 5

_THRESHOLD = 0.9

_MAX_ENERGY = 2.0

_ACTIONS = [
    SimObject.Action.EAT,
    SimObject.Action.MOVE,
    SimObject.Action.TURN_LEFT,
    SimObject.Action.TURN_RIGHT,
    SimObject.Action.DO_NOTHING
]


class NodeType(Enum):

    INPUT = 'in'

    OUTPUT = 'out'


def _vectorize_object(obj):
    return [int(Food.is_me(obj)), int(Wall.is_me(obj)), int(Empty.is_me(obj))]


def _vectorize_direction(direction):
    return [
        int(direction == Direction.EAST),
        int(direction == Direction.NORTH),
        int(direction == Direction.WEST),
        int(direction == Direction.SOUTH)
    ]


def _vectorize_energy(energy):
    out = [0, 0, 0, 0, 0]
    ind = int(energy * 5.0 / _MAX_ENERGY)
    out[ind if ind < 5 else 4] = 1
    return out


class NeatAgent(SimAgent):
    """ Fill in later
    """

    CONNECTIONS_KEY = "connections"

    def __init__(self, state, *args, **kwds):
        super().__init__(state, *args, **kwds)
        self._monitor['_energy'] = _MAX_ENERGY
        self._monitor['_direction'] = Direction.NORTH
        self._nodes, self._connections = state["genome"]
        self._states = defaultdict(lambda: 0)

    def _winner_takes_all(self, states):
        print(states)
        maximum = 0
        ind = 0
        for nid, state in states.items():
            if state > maximum:
                maximum = state
                ind = nid
        return {nid: 1 if nid == ind else 0 for nid in states.keys()}

    def _integrate_network(self, input_state):
        # Get save input states
        for i, in_state in enumerate(input_state):
            self._states[i] = in_state

        out_state = defaultdict(lambda: 0.0)
        for in_id, out_id, weight, _ in self._connections:
            out_state[out_id] += self._states[in_id] * weight

        # print(out_state)
        self._states = {
            nid: 1 if state > _THRESHOLD else 0
            for nid, state in out_state.items()}
        self._states.update(
            self._winner_takes_all(
                {nid: out_state[nid]
                    for nid, n_type in self._nodes
                    if n_type == NodeType.OUTPUT}))

    def add_energy(self, energy):
            super().add_energy(energy)
            # Set self._energy, but monitor the change.
            new_energy = self._energy + energy
            self._monitor['_energy'] = (
                _MAX_ENERGY if new_energy > _MAX_ENERGY else new_energy)

    def get_visible(self, objects_map):
        """
        """
        objects_list = []
        # Turn left and move forward
        current_direction = turn(self.direction, False)
        current_position = self._position.move(current_direction)
        objects_list.append(
            objects_map.get_object_for_position(current_position))
        # Turn right and move forward
        current_direction = turn(current_direction, True)
        current_position = current_position.move(current_direction)
        objects_list.append(
            objects_map.get_object_for_position(current_position))
        # Turn right and move forward
        current_direction = turn(current_direction, True)
        current_position = current_position.move(current_direction)
        objects_list.append(
            objects_map.get_object_for_position(current_position))
        # Move forward
        current_position = current_position.move(current_direction)
        objects_list.append(
            objects_map.get_object_for_position(current_position))
        # Turn right and move forward
        current_direction = turn(current_direction, True)
        current_position = current_position.move(current_direction)
        objects_list.append(
            objects_map.get_object_for_position(current_position))

        return objects_list

    def start_turn(self, objects_map):
        """
        :type objects_map: ObjectsMap
        """
        super().start_turn(objects_map)
        # Reduce energy.
        self._energy -= 0.1  # do not tell the monitor
        print(self._connections)
        if self._energy <= 0.0001:
            self._action = self.Action.DIE
        else:
            input_state = list(
                chain.from_iterable(
                    map(_vectorize_object, self.get_visible(objects_map))))
            input_state.extend(_vectorize_direction(self.direction))
            input_state.extend(_vectorize_energy(self._energy))
            self._integrate_network(input_state)
            # Choose what to do.
            out_states = [
                self._states[nid]
                for nid, n_type in self._nodes if n_type == NodeType.OUTPUT]
            print(self._states)
            print(out_states)
            self._action = _ACTIONS[out_states.index(1)]


NeatAgent.register()
