# -*- coding: utf-8 -*-
from random import choice, random

from ..position import directions
from .empty import Empty
from .food import Food
from .sim_object import SimObject
from .sim_agent import SimAgent

class ClassicalAiAgent(SimAgent):
    """ Hard-coded AI for solving the maps. No learning at all. Intended for benchmarking

    The agent is not aware of the map from the begining, but maitains an internal map
    based on its exploration.

    The agent has a limited life time (100 turns). It can eat food (10 turns
    for each 1 energy point).

    The score is measured in move actions plus eat actions.
    """

    def __init__(self, state, *args, **kwds):
        super().__init__(state, *args, **kwds)
        self._energy = 10.0
        self._monitor['_direction'] = choice(directions)
        self._internalMap = None

    def explore(self, objects_map):
        '''
        Update the internal map with the visible objects
        '''
        forward = self._position.move(self._direction)
        left = self._position.move(turn(self._direction, False))
        right = self._position.move(turn(self._direction, True)))
        for pos in [forward,left,right]:
            self._internalMap[pos.y][pos.x] = objects_map.get_object_for_position(pos)

    def bfs(self):
        '''
        Gives a list of all known foods on the map, in the order of distance as measured
        by the number of actions required from the current position.
        '''
        dist = {(self._position,self._direction) : 0}
        parent = {(self._position,self._direction) : None}
        queue = [(self._position,self._direction)]
        food = []
        while len(queue) > 0:
            current = queue.pop(0)
            moves = [
                (current[0], turn(current[1], False)),
                (current[0], turn(current[1], True)),
                (current[0].move(current[1]), current[1])
            ]
            for move in moves:
                obj = self._internalMap[move[0].y][move[0].y]
                #Assume unexplored (marked by None) cells are empty until proved otherwise
                if obj is None or Empty.is_me(obj):
                    if move not in dist:
                        dist[move] = dist[current] + 1
                        parent[move] = current
                        queue.append(move)
            if Food.is_me(self._internalMap[moves[2][0].y][moves[2][0].x]):
                food.append((dist[current]+1,current))
        return sorted(food), parent
    
    def start_turn(self, objects_map):
        """
        :type objects_map: ObjectsMap
        """
        super().start_turn(objects_map)

        if self._internalMap is None:
            self._internalMap = [[None]*objects_map._width for _ in range(objects_map._height)]

        # Reduce energy.
        self._energy -= 0.1  # do not tell the monitor
        if self._energy <= 0.0001:
            self._action = self.Action.DIE
            return

        self.explore(self,objects_map)
        
        visible = self.get_visible(objects_map)

        # What could the agent do? Nothing or turn are always possible.
        actions = [
            self.Action.DO_NOTHING,
            self.Action.TURN_LEFT
            if random() >= 0.5 else self.Action.TURN_RIGHT]
        
        if any(map(Food.is_me, visible)):
            actions.append(self.Action.EAT)
        if any(map(Empty.is_me, visible)):
            actions.append(self.Action.MOVE)
                
            # Make probability check for each action.
            actions = [
                a for a in actions if random() < self._probabilities[a]]
        # Choose what to do.
        self._action = choice(actions) if actions else self.Action.DO_NOTHING

ClassicalAiAgent.register()
