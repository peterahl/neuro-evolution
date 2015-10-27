#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from ne_simulator.sim_mixins import StepsLimiter
from ne_simulator.sim_mixins.map_printer import MapPrinter
from ne_simulator.sim_objects.ann_simple_agent import \
    ANNSimpleAgent  # @UnusedImport
from ne_simulator.simulator import Simulator
from types import ModuleType
from sys import modules
from ne_simulator.evolution import SIMULATOR_CLASS, Evolution, EVOLUTION_CLASS,\
    SIMULATIONS_COUNT, SCENARIOS, SIMULATOR_CONFIGURATION
from ne_simulator.sim_objects.score_monitor import ScoreMonitor
from random import choice, random, randint


_SIMULATION_COUNTS = 6  # agents for a generation

_PARENTS_FOR_NEXT_GENERATION = 3  # best agents

_MAX_GENERATIONS = 100

_RANDOMIZE_DELTA = 0.1

_NOICE_COUNT = 50


class FitnessScoreMonitor(ScoreMonitor):
    
    def calculate_score(self):
        score = 1.0
        if self.did_change('_energy'):
            score += 1
        if self.did_change('_position'):
            score += 1
        return score


class ANNSimpleEvolution(Evolution):

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
        should_continue = True
        new_contexts = None
        self._generation_count += 1
        if self._generation_count >= _MAX_GENERATIONS:
            should_continue = False
        if should_continue:
            agents_contexts = sorted(
                [sim_ctx[CONTEXT_KEY_PREFIX]
                    for sim_ctx in simulations_contexts],
                key=lambda x: x[SCORE_KEY])
            print(*[c[SCORE_KEY] for c in agents_contexts])
            best_weights = [
                c[WEIGHTS_KEY]
                for c in agents_contexts[-_PARENTS_FOR_NEXT_GENERATION:]]
            print(*[' '.join(['%.3f' % x for x in row]) for row in best_weights[-1][-5:]], sep='\n')
            new_weights = []
            for _ in range(_SIMULATION_COUNTS):
                weights = [[choice(best_weights)[row_nr][col_nr]
                        for col_nr in range(len(best_weights[0][0]))]
                    for row_nr in range(len(best_weights[0]))]
                for _ in range(_NOICE_COUNT):
                    row = choice(weights)
                    row[randint(0, len(row) - 1)] += (
                        random() * 2 * _RANDOMIZE_DELTA - _RANDOMIZE_DELTA)
                new_weights.append(weights)
            new_contexts = [{
                ANNSimpleAgent.CONTEXT_KEY_PREFIX: {
                    ANNSimpleAgent.WEIGHTS_KEY: weights}
                }
                for weights in new_weights]
        return should_continue, new_contexts

def main():
    class Sim(StepsLimiter, MapPrinter, Simulator):
        pass

    # Create and add module to be used by the run function.
    main_module = ModuleType("main")
    main_module.FitnessScoreMonitor = FitnessScoreMonitor
    main_module.ANNSimpleEvolution = ANNSimpleEvolution
    modules["main"] = main_module

    with open('configurations/random_agent.json') as jfile:
        scenario = json.load(jfile)

    scenario["until_no_objects"] = ANNSimpleAgent
    scenario["parameters"] = {
        (24, 13): ([], {'score_monitor_class':'main.FitnessScoreMonitor'})}
    configuration =  {
        EVOLUTION_CLASS: "main.ANNSimpleEvolution",
        SIMULATIONS_COUNT: _SIMULATION_COUNTS,
        SCENARIOS: [{
            SIMULATOR_CLASS: (
                    "ne_simulator.sim_mixins.until_no_objects.UntilNoObjects",
                    "ne_simulator.simulator.Simulator"),
            SIMULATOR_CONFIGURATION: scenario}],
    }
    Evolution.get_instance(configuration).run()

if __name__ == '__main__':
    main()
