# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue as ProcessQueue  # @UnresolvedImport
from queue import Queue
from threading import Thread


SIMULATOR_CLASS = "simulator_class"

SCENARIOS = "scenarios"

SIMULATOR_CONFIGURATION = "configuration"

SIMULATIONS_COUNT = "simulations_count"


def _run_simulation(queue, simulator_class, configuration, state):
    # Run and put resulting state information into queue.
    queue.put(simulator_class(configuration, state).run())


class Evolution():

    def __init__(self, scenarios, simulators_count, **kwds):
        self._scenarios = scenarios
        self._simulation_states = [{} for _ in range(simulators_count)]

    def scenario_start(self):
        """ New scenario, reset any evolve state. """
        pass

    def evolve(self, simulation_states):
        """ Return should_continue and new states. """
        return False, None

    def _gen_threads(self, simulator_class, configuration):
        queues = [Queue() for _ in range(len(self._simulation_states))]
        simulators = [
            Thread(
                target=_run_simulation,
                args=(queue, simulator_class, configuration, state))
            for queue, state in zip(queues, self._simulation_states)]
        return queues, simulators

    def _gen_processes(self, simulator_class, configuration):
        queues = [ProcessQueue() for _ in range(len(self._simulation_states))]
        simulators = [
            Process(
                target=_run_simulation,
                args=(queue, simulator_class, configuration, state))
            for queue, state in zip(queues, self._simulation_states)]
        return queues, simulators

    def _run_one_generation(self, simulator_class, configuration):
        """ Spawn as many threads as there are states, run the simulators in
        parallel, read the new state and wait for the threads to finish.
        """
        queues, simulators = self._gen_processes(
            simulator_class, configuration)
        for t in simulators:
            t.start()
        self._simulation_states = [q.get() for q in queues]
        for t in simulators:
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
            should_continue = None
            while should_continue is None or should_continue:
                self._run_one_generation(
                    scenario[SIMULATOR_CLASS],
                    scenario[SIMULATOR_CONFIGURATION])
                should_continue, self._simulation_states = self.evolve(
                    self._simulation_states)

# TODO: add a function to show off the best agent?
# TODO: add a player for showing recorded maps (agent behavior)
