# -*- coding: urf-8 -*-
from queue import Queue
from threading import Thread


EVALUATION_FUNCTION = "eval"

SIMULATOR_CLASS = "simulator"

CONFIGURATION = "configuration"

SIMULATIONS_COUNT = "simulations_count"


def run_simulation(q, simulator_class, configuration, init_state):
    res_state = simulator_class(configuration, init_state).run()
    # put resulting state information into queue
    q.put(res_state)

def run(configuration):
    """ Run several simulation scenarios.

    Using the configuration:
    - run first scenario until condition function is satisfied
    - run next scenario if there is one

    A scenario consists of a number of simulations run in parallel. After each
    round all data needs to be combined and a new round can be run.

    Data needs to be stored in files by the agents themselves. They can us the
    scenario and simulation number to id themselves between rounds and
    scenarios.
    """
    for scenario_nr, scenario in enumerate(configuration):
        evaluation = __import__(scenario[EVALUATION_FUNCTION])
        Simulator = __import__(scenario[SIMULATOR_CLASS])
        simulations_count = scenario[SIMULATIONS_COUNT]
        sim_states = [{} for _ in range(simulations_count)]
        queues = [Queue() for _ in range(simulations_count)]
        should_continue = None
        round_nr = 0
        while should_continue is None or should_continue:
            simulator_threads = [
                Thread(
                    target=run_simulation,
                    args=(
                        q, Simulator, scenario[CONFIGURATION], s))
                for q, s in zip(queues, sim_states)]
            for t in simulator_threads:
                t.start()
            for i, q in enumerate(queues):
                sim_states[i] = q.get()
            for t in simulator_threads:
                t.join()
            should_continue = #evaluation(sim_states)
            round_nr += 1

# TODO: add a function to show off the best agent?
# TODO: add a player for showing recorded maps (agent behavior)
