# -*- coding: utf-8 -*-
from ne_simulator import ScoreMonitor


class Monitor(ScoreMonitor):

    def calculate_score(self):
        score = 0
        current_energy = self._current.get('_energy')
        last_energy = self._last.get('_energy')
        if (current_energy is not None and last_energy is not None and
                current_energy > last_energy):
            score += 3
        if self.did_change('_position'):
            score += 1
        return score
