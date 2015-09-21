# -*- coding: utf-8 -*-


class StepsLimiter():
    """ Limit the amount of steps that the simulation runs.

    Configuration:
     - steps_limiter_steps: how many steps the simulation should run. Defaults
         to 0.
    """

    def __init__(self, configuration, state):
        self._steps = configuration.get("steps_limiter_steps", 0)
        super().__init__(configuration, state)

    def should_run(self):
        self._steps -= 1
        return self._steps >= 0
