# -*- coding: utf-8 -*-


class UntilNoObjects():
    """ Run until there is no object of the given types left.

    Configuration:
     - until_no_objects: list of objects types that have to be present in order
       for the simulation to continue running.
    """

    def __init__(self, configuration, state):
        self._until_objects = configuration.get("until_no_objects", None)
        super().__init__(configuration, state)

    def should_run(self):
        if not self._until_objects:
            return False
        return any(
            map(lambda x: isinstance(x, self._until_objects), self._map))
