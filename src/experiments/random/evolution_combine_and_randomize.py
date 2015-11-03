# -*- coding: utf-8 -*-
from random import random, choice

from ne_simulator import Evolution as EvolutionBase
from ne_simulator.sim_objects.random_agent import RandomAgent


_PARENTS_FOR_NEXT_GENERATION = 2  # best agents

_RANDOMIZE_DELTA = 0.02

_MAX_GENERATIONS = 10


def _randomize(value):
    value += random() * 2 * _RANDOMIZE_DELTA - _RANDOMIZE_DELTA
    return value


def _normalize(value):
    if value > 1.0:
        value = 1.0
    if value < 0.0:
        value = 0.0
    return value


class Evolution(EvolutionBase):

    def __init__(self, scenarios, simulators_count, **kwds):
        super().__init__(scenarios, simulators_count, **kwds)
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
