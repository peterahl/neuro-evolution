# -*- coding: utf-8 -*-
from ne_simulator.simulator import Simulator
from ne_simulator.sim_mixins import StepsLimiter, MapRecorder


class RecorderSimulator(StepsLimiter, MapRecorder, Simulator):
    pass
