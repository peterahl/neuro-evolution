# -*- coding: urf-8 -*-
from queue import Queue
from threading import Thread


EVOLVE_FUNCTION = "evolve"

SIMULATOR_CLASS = "simulator"

CONFIGURATION = "configuration"

SIMULATIONS_COUNT = "simulations_count"


def _run_simulation(queue, simulator_class, configuration, state):
    # Run and put resulting state information into queue.
    queue.put(simulator_class(configuration, state).run())


def _run_one_round(simulator_class, configuration, states):
    """ Spawn as many threads as there are states, run the simulators in
    parallel, read the new state and wait for the threads to finish.

    Returns the new simulation states.
    """
    queues = [Queue() for _ in range(len(states))]
    simulator_threads = [
        Thread(
            target=_run_simulation,
            args=(queue, simulator_class, configuration, state))
        for queue, state in zip(queues, states)]
    for t in simulator_threads:
        t.start()
    new_states = [q.get() for q in queues]
    for t in simulator_threads:
        t.join()
    return new_states


def run(configuration):
    """ Run several simulation scenarios.

    Using the configuration:
    - run first scenario until condition function is satisfied
    - run next scenario if there is one
    - use a dictionary as "simulation state" where SomObject instances can pass
        data from one run to the next one

    A scenario consists of a number of simulations run in parallel. After each
    round a "evolution" function can manipulate the simulation states and
    decide if another round of the same scenario should be run (a new
    generation, so to speak).
    """
    for scenario in enumerate(configuration):
        evolve = __import__(scenario[EVOLVE_FUNCTION])
        simulator_class = __import__(scenario[SIMULATOR_CLASS])
        simulators_count = scenario[SIMULATIONS_COUNT]
        simulator_configuration = scenario[CONFIGURATION]
        simulation_states = [{} for _ in range(simulators_count)]
        should_continue = None
        while should_continue is None or should_continue:
            simulation_states = _run_one_round(
                simulator_class, simulator_configuration, simulation_states)
            should_continue = evolve(simulation_states)

# TODO: add a function to show off the best agent?
# TODO: add a player for showing recorded maps (agent behavior)
