# -*- coding: utf-8 -*-
from .sim_object import SimObject


class Food(SimObject):

    SYMBOL = '+'

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self._energy = 1.0

    def remove_energy(self):
        energy = self._energy
        self._energy = 0
        return energy

    def action(self):
        return self.Action.DIE if self._energy == 0 else None


Food.register()
