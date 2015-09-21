# -*- coding: utf-8 -*-
from queue import Queue
from threading import Thread
from importlib import import_module


EVOLUTION_CLASS = "evolution_class"

SCENARIOS = "scenarios"

SIMULATOR_CLASS = "simulator_class"

SIMULATOR_CONFIGURATION = "configuration"

SIMULATIONS_COUNT = "simulations_count"


def _import_obj(object_from_package):
    elements = object_from_package.split('.')
    if len(elements) < 2:
        raise RuntimeError(
            'Can not auto import {}'.format(object_from_package))
    obj = elements[-1]
    package = ".".join(elements[:-1])
    return getattr(import_module(package), obj)


def _run_simulation(queue, simulator_class, configuration, state):
    # Run and put resulting state information into queue.
    queue.put(simulator_class(configuration, state).run())


class Evolution():

    def __init__(self, scenarios, simulators_count):
        super().__init__()
        self._scenarios = scenarios
        self._simulation_states = [{} for _ in range(simulators_count)]

    def scenario_start(self):
        """ New scenario, reset any evolve state. """
        pass

    def evolve(self, simulation_states):
        """ Return should_continue and new states. """
        return False, None

    def _run_one_generation(self, simulator_class, configuration):
        """ Spawn as many threads as there are states, run the simulators in
        parallel, read the new state and wait for the threads to finish.
        """
        queues = [Queue() for _ in range(len(self._simulation_states))]
        simulator_threads = [
            Thread(
                target=_run_simulation,
                args=(queue, simulator_class, configuration, state))
            for queue, state in zip(queues, self._simulation_states)]
        for t in simulator_threads:
            t.start()
        self._simulation_states = [q.get() for q in queues]
        for t in simulator_threads:
            t.join()

    def run(self):
        """ Run several simulation scenarios.

        Using the configuration:
        - run first scenario until condition function is satisfied
        - run next scenario if there is one
        - use a dictionary as "simulation state" where SomObject instances can
            pass data from one run to the next one
        - the simulation state should contain score information for the evolve
            function as well, which the should_run function could provide

        A scenario consists of a number of simulations run in parallel. After
        each round a "evolution" function can manipulate the simulation states
        and decide if another round of the same scenario should be run (a new
        generation, so to speak).
        """
        for scenario in self._scenarios:
            self.scenario_start()
            simulator_class = _import_obj(scenario[SIMULATOR_CLASS])
            simulator_configuration = scenario[SIMULATOR_CONFIGURATION]
            should_continue = None
            while should_continue is None or should_continue:
                self._run_one_generation(
                    simulator_class, simulator_configuration)
                should_continue, self._simulation_states = self.evolve(
                    self._simulation_states)

    @staticmethod
    def get_instance(configuration):
        return _import_obj(configuration[EVOLUTION_CLASS])(
            configuration[SCENARIOS], configuration[SIMULATIONS_COUNT])


# TODO: add a function to show off the best agent?
# TODO: add a player for showing recorded maps (agent behavior)
