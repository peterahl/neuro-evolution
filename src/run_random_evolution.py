#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice, random
from sys import modules
from types import ModuleType

from ne_simulator.evolution import SIMULATIONS_COUNT, Evolution, \
    EVOLUTION_CLASS, SIMULATOR_CLASS, SIMULATOR_CONFIGURATION, SCENARIOS
from ne_simulator.sim_mixins.until_no_objects import UntilNoObjects
from ne_simulator.sim_objects.food import Food
from ne_simulator.sim_objects.random_agent import RandomAgent, state_to_list, \
    list_to_state
from ne_simulator.simulator import Simulator


_SIMULATION_COUNTS = 6  # agents for a generation

_PARENTS_FOR_NEXT_GENERATION = 3  # best agents

_RANDOMIZE_DELTA = 0.02

_MAX_GENERATIONS = 100


class TestSimulator(UntilNoObjects, Simulator):
    pass


def _randomize(value):
    value += random() * 2 * _RANDOMIZE_DELTA - _RANDOMIZE_DELTA
    return value


def _normalize(value):
    if value > 1.0:
        value = 1.0
    if value < 0.0:
        value = 0.0
    return value


class RandomAgentEvolution(Evolution):

    def __init__(self, scenarios, simulators_count):
        super().__init__(scenarios, simulators_count)
        self._generation_count = 0

    def scenario_start(self):
        super().scenario_start()
        self._generation_count = 0

    def evolve(self, simulation_states):
        should_continue = True
        new_states = None
        self._generation_count += 1
        if self._generation_count >= _MAX_GENERATIONS:
            should_continue = False
        if should_continue:
            STATE_KEY = RandomAgent.STATE_KEY  # shortcut
            SCORE_KEY = RandomAgent.SCORE_KEY  # shortcut
            simulation_states = sorted(
                simulation_states, key=lambda x: x[SCORE_KEY])
            print(*[s[SCORE_KEY] for s in simulation_states])
            best_states = [
                state_to_list(b[STATE_KEY])
                for b in simulation_states[-_PARENTS_FOR_NEXT_GENERATION:]]
            print("\n".join([str(b) for b in best_states]), end="\n\n")
            # Create new states, using the parameters of the best.
            params_count = len(best_states[0])
            new_states = [
                {STATE_KEY:
                    list_to_state([
                        _normalize(_randomize(choice(best_states)[i]))
                        for i in range(params_count)])}
                for _ in simulation_states]
        return should_continue, new_states


def main():
    # Create and add module to be used by the run function.
    main_module = ModuleType("main")
    main_module.TestSimulator = TestSimulator
    main_module.RandomAgentEvolution = RandomAgentEvolution
    modules["main"] = main_module
    # Build scenarios/configuration.
    configuration = {
        EVOLUTION_CLASS: "main.RandomAgentEvolution",
        SIMULATIONS_COUNT: _SIMULATION_COUNTS,
        SCENARIOS: [
            {SIMULATOR_CLASS: "main.TestSimulator",
                SIMULATOR_CONFIGURATION: {
                    "map": [
                        "#########",
                        "#++     #",
                        "#       #",
                        "# r  ####",
                        "#    ++ #",
                        "#       #",
                        "##     +#",
                        "#+      #",
                        "#########",
                    ],
                    "until_no_objects": (RandomAgent, Food),
                },
            },  # @IgnorePep8
        ],
    }
    # Run it.
    Evolution.get_instance(configuration).run()


if __name__ == '__main__':
    main()
