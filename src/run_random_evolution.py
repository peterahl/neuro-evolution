#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice, random
from sys import modules
from types import ModuleType

from ne_simulator.evolution import SIMULATIONS_COUNT, Evolution, \
    EVOLUTION_CLASS, SIMULATOR_CLASS, SIMULATOR_CONFIGURATION, SCENARIOS
from ne_simulator.sim_objects import Food, ScoreMonitor
from ne_simulator.sim_objects.random_agent import RandomAgent


_SIMULATION_COUNTS = 6  # agents for a generation

_PARENTS_FOR_NEXT_GENERATION = 3  # best agents

_RANDOMIZE_DELTA = 0.02

_MAX_GENERATIONS = 100


def _randomize(value):
    value += random() * 2 * _RANDOMIZE_DELTA - _RANDOMIZE_DELTA
    return value


def _normalize(value):
    if value > 1.0:
        value = 1.0
    if value < 0.0:
        value = 0.0
    return value


class MoveAndEatScoreMonitor(ScoreMonitor):

    def calculate_score(self):
        score = 0
        if self.did_change('_energy'):
            score += 1
        if self.did_change('_position'):
            score += 1
        return score


class RandomAgentEvolution(Evolution):

    def __init__(self, scenarios, simulators_count):
        super().__init__(scenarios, simulators_count)
        self._generation_count = 0

    def scenario_start(self):
        super().scenario_start()
        self._generation_count = 0

    def evolve(self, simulations_contexts):
        """ Find agents with highest score and create next generation out of
        them.

        Each context in the list should contain at least:
          {RandomAgent.CONTEXT_KEY_PREFIX: {
              RandomAgent.SCORE_KEY: score,
              RandomAgent.PROBABILITIES_KEY: probabilities}}
        For example:
            {'agent': {
                'probabilities': [
                    0.6264288465185096, 0.5026548291908151,
                    0.46334352233222653, 0.5435121209334894,
                    0.4466975141611824],
                'score': 28}}
        """
        CONTEXT_KEY_PREFIX = RandomAgent.CONTEXT_KEY_PREFIX  # shortcut
        SCORE_KEY = RandomAgent.SCORE_KEY  # shortcut
        PROBABILITIES_KEY = RandomAgent.PROBABILITIES_KEY  # shortcut
        should_continue = True
        new_states = None
        self._generation_count += 1
        if self._generation_count >= _MAX_GENERATIONS:
            should_continue = False
        if should_continue:
            # Extract all agent contexts and sort them
            agents_contexts = sorted(
                [sim_ctx[CONTEXT_KEY_PREFIX]
                    for sim_ctx in simulations_contexts],
                key=lambda x: x[SCORE_KEY])
            print(*[c[SCORE_KEY] for c in agents_contexts])
            # Make a list of the best probabilities.
            best_probabilities = [
                c[PROBABILITIES_KEY]
                for c in agents_contexts[-_PARENTS_FOR_NEXT_GENERATION:]]
            print("\n".join(map(str, best_probabilities)), end="\n\n")
            # Create new states, using the parameters of the best. Add a bit
            # of random mutation to each value, taking care to keep it within
            # 0 and 1!
            params_count = len(best_probabilities[0])
            new_states = [
                {CONTEXT_KEY_PREFIX: {
                    PROBABILITIES_KEY: [
                        _normalize(_randomize(choice(best_probabilities)[i]))
                        for i in range(params_count)]}}
                for _ in simulations_contexts]
        return should_continue, new_states


def main():
    # Create and add module to be used by the run function.
    main_module = ModuleType("main")
    main_module.MoveAndEatScoreMonitor = MoveAndEatScoreMonitor
    main_module.RandomAgentEvolution = RandomAgentEvolution
    modules["main"] = main_module
    # Build scenarios/configuration.
    configuration = {
        EVOLUTION_CLASS: "main.RandomAgentEvolution",
        SIMULATIONS_COUNT: _SIMULATION_COUNTS,
        SCENARIOS: [
            {SIMULATOR_CLASS: (
                    "ne_simulator.sim_mixins.until_no_objects.UntilNoObjects",
                    "ne_simulator.simulator.Simulator"),
                SIMULATOR_CONFIGURATION: {
                    "map": [
                        "#########",
                        "#++     #",
                        "#       #",
                        "# a  ####",
                        "#    ++ #",
                        "#       #",
                        "##     +#",
                        "#+      #",
                        "#########",
                    ],
                    "until_no_objects": (RandomAgent, Food),
                    # TODO: move the score class into the simulator?
                    "parameters": {
                        (2, 3): (
                            [],
                            {"score_monitor_class":
                                "main.MoveAndEatScoreMonitor"})
                    }
                },
            },  # @IgnorePep8
        ],
    }
    # Run it.
    Evolution.get_instance(configuration).run()


if __name__ == '__main__':
    main()
