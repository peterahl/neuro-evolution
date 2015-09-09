# -*- coding: utf-8 -*-


# Enable multi inheritance for Simulator: all __init__ need too look like this.
class SimBase():

    def __init__(self, configuration):
        super().__init__()
