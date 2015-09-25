# -*- coding: utf-8 -*-
from weakref import ref


class ScoreMonitor():
    """ Base class for a agent monitor and score class.

    All values from the agent that should be used to calculate the score for
    the agent need to go through the monitor like so:
    in the agent call `self._monitor.['_my_field'] = value`
    instead of setting it directly `self._my_field = value`

    Setting a value on the monitor will set the value in the agent as well:
    `self._monitor.['_my_field'] = value` equals to `self._my_field = value`
    from the agents point of view.

    This way the monitor can keep track of the current and last value for each
    field/variable and the function calculating the score can make use of
    `_current` and `_last` to do its work.

    The SimAgent class for example records `_direction`, `_energy` and
    `_position`.
    """

    def __init__(self, agent):
        self._agent = ref(agent)
        self._current = {}
        self._last = {}
        self._objects_map = None

    def __setitem__(self, key, value):
        """ Record the value into _current and forward the set operation to
        the agent.
        """
        self._current[key] = value
        agent = self._agent()
        if agent:
            setattr(agent, key, value)

    @property
    def objects_map(self):
        return ref() if ref is not None else None

    @objects_map.setter
    def objects_map(self, objects_map):
        # Usage of ref is probably not strictly necessary, but since it should
        # not be stored outside the original SimObject.start_turn function ...
        self._objects_map = ref(objects_map)

    def did_change(self, field_name):
        """ Check if the field exists in both _current and _last return
        whenever the values differ or not.

        :rtype: bool
        """
        if field_name in self._current and field_name in self._last:
            return self._current[field_name] != self._last[field_name]
        return False

    def calculate_score(self):
        """ Calculate the score using `_current` and `_last`.

        Each contains the monitored agent fields, changed this round and what
        the last value has been.

        For checking the objects of the current map consult `self.objects_map`.

        :rtype: float
        """
        return 0.0

    def evaluate(self):
        """ End the round and return the score.

        Ending a round means update `_last` with `_current` and clear
        `_current`.

        :rtype: float
        """
        score = self.calculate_score()
        self._last.update(self._current)
        self._current.clear()
        self._objects_map = None
        return score
