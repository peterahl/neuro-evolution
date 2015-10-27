# -*- coding: utf-8 -*-
from ..import_util import import_obj
from ..position import Direction, turn
from .score_monitor import ScoreMonitor
from .sim_object import SimObject


class SimAgent(SimObject):
    """ Base class that has a simulation context, direction, energy and a
    monitor to calculate the agents score.
    """

    SYMBOL = "a"

    # The key prefix for the agent context (dictionary) within the simulation
    # context.
    CONTEXT_KEY_PREFIX = "agent"

    # The key for the agents score within the agent context.
    SCORE_KEY = "score"

    def __init__(self, context, *args, **kwds):
        """ Adds some agent related object fields and initializes the state.

        New fields:
        - _energy = 0
        - _direction = Direction.NORTH
        - _ctx = {self.SCORE_KEY: 0}
        - _action = SimObject.Action.DO_NOTHING

        TODO: add initial energy and score to the configuration?

        Configuration: (kwds)
        - context_prefix: [string] adds to CONTEXT_KEY_PREFIX before accessing
            the simulation context (where to store the context of the agent)
        - initial_direction: [Direction] value for _direction, default is NORTH
        - score_monitor_class: [ScoreMonitor] a ScoreMonitor derived class that
            can calculate the agents score
        """
        super().__init__(context, *args, **kwds)
        ctx_key = self.CONTEXT_KEY_PREFIX + kwds.get("context_prefix", "")
        ctx = context.get(ctx_key)
        if ctx is None:
            ctx = context[ctx_key] = {}
        self._ctx = ctx
        self._ctx[self.SCORE_KEY] = 0
        self._direction = kwds.get("initial_direction", Direction.NORTH)
        self._energy = 0
        monitor_class = kwds.get("score_monitor_class")
        monitor_class = (
            import_obj(monitor_class)
            if monitor_class is not None else ScoreMonitor)
        self._monitor = monitor_class(self)
        self._position = None

    @property
    def direction(self):
        return self._direction

    def set_direction(self, direction):
        super().set_direction(direction)
        self._monitor['_direction'] = direction  # self._direction = direction

    def add_energy(self, energy):
        super().add_energy(energy)
        # Set self._energy, but monitor the change.
        self._monitor['_energy'] = self._energy + energy

    def get_visible(self, objects_map):
        """ Get 3 visible tiles.

        :return: the front, left and right object considering self._direction
        :rtype: (SimObject, SimObject, SimObject)
        """
        # What is visible to the agent?
        front = objects_map.get_object_for_position(
            self._position.move(self._direction))
        left = objects_map.get_object_for_position(
            self._position.move(turn(self._direction, False)))
        right = objects_map.get_object_for_position(
            self._position.move(turn(self._direction, True)))
        return (front, left, right)

    def start_turn(self, objects_map):
        """ Monitor _position and send the objects_map to the monitor. """
        super().start_turn(objects_map)
        self._monitor.objects_map = objects_map  # keeps only a weak ref
        self._monitor['_position'] = objects_map.get_position_for_object(self)

    def action(self):
        """ This calculates a score for this round and returns the action from
        self._action .
        """
        super().action()
        score = self._monitor.evaluate()
        self._ctx[self.SCORE_KEY] += score
        return self._action
