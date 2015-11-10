# -*- coding: utf-8 -*-
from random import random, choice, randint

from ne_simulator import Evolution as EvolutionBase
from ne_simulator.sim_objects.ann_structure_agent import ANNStructuredAgent


_MAX_GENERATIONS = 10


def _randomize(value, delta):
    value += random() * 2 * delta - delta
    return value


def _normalize(value, lower, upper):
    if value > upper:
        value = upper
    if value < lower:
        value = lower
    return value


def _avg_min(mm1, mm2):
    min1, _ = mm1
    min2, _ = mm2
    return (min1 + min2) / 2.0


def _avg_max(mm1, mm2):
    _, max1 = mm1
    _, max2 = mm2
    return (max1 + max2) / 2.0


def _combine(a1, a2):
    return {
        (_normalize(_randomize(_avg_min(a1[k], a2[k]), delta), lower, upper),
            _normalize(
                _randomize(_avg_max(a1[k], a2[k]), delta), lower, upper))
        for k, (_, _, lower, upper, delta)
        in ANNStructuredAgent.MIN_MAX_TEMPLATE
    }


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
            {
                ANNStructuredAgent.CONTEXT_KEY_PREFIX: {
                    ANNStructuredAgent.SCORE_KEY: score,
                    ANNStructuredAgent.MIN_MAX_KEY: min_max_limits
                }
            }
        For example:
            {
                "agent": {
                    "min_max": {
                        "nodes": (8, 14),
                        "layers": (3, 6),
                        "mu": (0.4, 0.5),
                        "sigma": (0.25, 0.3),
                        "outdegree": (1, 4)
                    },
                    "score": 28
                }
            }
        """
        CONTEXT_KEY_PREFIX = ANNStructuredAgent.CONTEXT_KEY_PREFIX  # shortcut
        SCORE_KEY = ANNStructuredAgent.SCORE_KEY  # shortcut
        MIN_MAX_KEY = ANNStructuredAgent.MIN_MAX_KEY  # shortcut
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
            best = [
                c[MIN_MAX_KEY]
                for c in agents_contexts[-len(agents_contexts) // 2:]]
            # Create new states, using the parameters of the best. Add a bit
            # of random mutation to each value, taking care to keep it within
            # the specified limits.
            new_states = []
            for _ in simulations_contexts:
                best_choice = list(best)
                a1 = best_choice.pop(randint(len(best_choice) - 1))
                a2 = best_choice.pop(randint(len(best_choice) - 1))
                new_states.append(
                    {CONTEXT_KEY_PREFIX: {MIN_MAX_KEY: _combine(a1, a2)}})
        return should_continue, new_states
