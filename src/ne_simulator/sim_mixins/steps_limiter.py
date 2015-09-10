# -*- coding: utf-8 -*-
from .base import SimBase


class StepsLimiter(SimBase):
    """ Limit the amount of steps that the simulation runs.

    Configuration:
     - steps_limiter_steps: how many steps the simulation should run. Defaults
         to 0.
    """

    def __init__(self, configuration):
        self._steps = configuration.get("steps_limiter_steps", 0)
        super().__init__(configuration)

    def should_run(self):
        self._steps -= 1
        return self._steps >= 0
