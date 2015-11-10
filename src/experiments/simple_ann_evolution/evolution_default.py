# -*- coding: utf-8 -*-
from random import choice, random

from ne_simulator import Evolution as EvolutionBase
from ne_simulator.sim_objects.ann_simple_agent import \
    ANNSimpleAgent


_RND_THRESHOLD = 0.3

_RND_AMOUNT = 0.05


def _randomize(w):
    if abs(w) < 0.00000001:
        return w
    if random() < _RND_THRESHOLD:
        w += random() * 2 * _RND_AMOUNT - _RND_AMOUNT
    return w


class Evolution(EvolutionBase):

    def __init__(
            self, scenarios, simulators_count, max_generations=10, **kwds):
        super().__init__(scenarios, simulators_count, **kwds)
        self._generation_count = 0
        self._max_generations = max_generations

    def scenario_start(self):
        super().scenario_start()
        self._generation_count = 0

    def evolve(self, simulations_contexts):
        """ Find agents with highest score and create next generation out of
        them.

        Each context in the list should contain at least:
          {ANNSimpleAgent.CONTEXT_KEY_PREFIX: {
              ANNSimpleAgent.SCORE_KEY: score,
              ANNSimpleAgent.WEIGHTS_KEY: weights}}
        For example:
            {'agent': {
                'weights': [[0, 0, ...], [0, 0, ...], ...],
                'score': 28}}
        """
        CONTEXT_KEY_PREFIX = ANNSimpleAgent.CONTEXT_KEY_PREFIX  # shortcut
        SCORE_KEY = ANNSimpleAgent.SCORE_KEY  # shortcut
        WEIGHTS_KEY = ANNSimpleAgent.WEIGHTS_KEY  # shortcut
        should_continue = self._generation_count < self._max_generations
        new_contexts = None
        if should_continue:
            agents_contexts = sorted(
                [sim_ctx[CONTEXT_KEY_PREFIX]
                    for sim_ctx in simulations_contexts],
                key=lambda x: x[SCORE_KEY])
            print(*[c[SCORE_KEY] for c in agents_contexts])
            best_weights = [
                c[WEIGHTS_KEY]
                for c in agents_contexts[-len(agents_contexts) // 2:]]
#             print(*[
#                 ' '.join(['%.3f' % x for x in row])
#                 for row in best_weights[-1][-5:]], sep='\n')
            new_weights = []
            for _ in range(len(simulations_contexts)):
                weights = choice(best_weights)
                weights = [
                    [_randomize(cell) for cell in row] for row in weights]
                new_weights.append(weights)
            new_contexts = [{
                ANNSimpleAgent.CONTEXT_KEY_PREFIX: {
                    ANNSimpleAgent.WEIGHTS_KEY: weights}
                }
                for weights in new_weights]
        self._generation_count += 1
        return should_continue, new_contexts
