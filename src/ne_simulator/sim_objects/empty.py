# -*- coding: utf-8 -*-
from .sim_object import SimObject


class Empty(SimObject):

    SYMBOL = " "


Empty.register()
