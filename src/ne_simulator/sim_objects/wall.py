# -*- coding: utf-8 -*-
from .sim_object import SimObject


class Wall(SimObject):

    SYMBOL = '#'


Wall.register()
