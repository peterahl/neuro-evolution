# -*- coding: utf-8 -*-
from ne_simulator import ScoreMonitor


class Monitor(ScoreMonitor):

    def calculate_score(self):
        score = 0
        if self.did_change('_energy'):
            score += 2
        if self.did_change('_position'):
            score += 1
        return score
