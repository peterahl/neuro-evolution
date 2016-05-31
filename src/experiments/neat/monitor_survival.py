# -*- coding: utf-8 -*-
from ne_simulator import ScoreMonitor


class Monitor(ScoreMonitor):

    def calculate_score(self):
        score = 1
        if ("_energy" in self._current and "_energy" in self._last and
                self._current["_energy"] > self._last["_energy"]):
            score += 3
        if self.did_change('_position'):
            score += 2
        return score
