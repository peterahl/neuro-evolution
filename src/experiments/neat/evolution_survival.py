# -*- coding: utf-8 -*-
from .evolution_default import Evolution as DefaultEvolution
from pprint import pprint
from random import randrange, choice
from itertools import groupby


_MAX_GENERATIONS = 6

_TOP_PERCENTAGE = 0.2


def _get_random_element(values):
    index = randrange(0, len(values))
    return values.pop(index)


class Evolution(DefaultEvolution):

    def __init__(self, *args, **kwds):
        kwds["multiprocessing"] = True
        super().__init__(*args, **kwds)
        self._generations_count = 0

    def evolve(self, simulation_states):
        """
        Agent state example:
        {'agent': {'genome': ([(0, <NodeType.INPUT: 'in'>),
                (1, <NodeType.INPUT: 'in'>),
                (2, <NodeType.INPUT: 'in'>),
                (3, <NodeType.INPUT: 'in'>),
                (4, <NodeType.INPUT: 'in'>),
                (5, <NodeType.INPUT: 'in'>),
                (6, <NodeType.INPUT: 'in'>),
                (7, <NodeType.INPUT: 'in'>),
                (8, <NodeType.INPUT: 'in'>),
                (9, <NodeType.INPUT: 'in'>),
                (10, <NodeType.INPUT: 'in'>),
                (11, <NodeType.INPUT: 'in'>),
                (12, <NodeType.INPUT: 'in'>),
                (13, <NodeType.INPUT: 'in'>),
                (14, <NodeType.INPUT: 'in'>),
                (15, <NodeType.INPUT: 'in'>),
                (16, <NodeType.INPUT: 'in'>),
                (17, <NodeType.INPUT: 'in'>),
                (18, <NodeType.INPUT: 'in'>),
                (19, <NodeType.INPUT: 'in'>),
                (20, <NodeType.INPUT: 'in'>),
                (21, <NodeType.INPUT: 'in'>),
                (22, <NodeType.INPUT: 'in'>),
                (23, <NodeType.INPUT: 'in'>),
                (24, <NodeType.OUTPUT: 'out'>),
                (25, <NodeType.OUTPUT: 'out'>),
                (26, <NodeType.OUTPUT: 'out'>),
                (27, <NodeType.OUTPUT: 'out'>),
                (28, <NodeType.OUTPUT: 'out'>)],
               [(8, 28, 0.686466201223033, 24),
                (11, 25, -0.7559113136656763, 22),
                (17, 28, -0.7808190967297456, 25),
                (19, 26, -0.18825390294811972, 26),
                (20, 26, 0.7843425320342479, 27)]),
        'score': 0.0}}
        """
        # pprint([s for s in states if s["agent"]["score"] > 20])
        states = [s["agent"] for s in simulation_states]
        # Keep best ones, based on score.
        states.sort(key=lambda x: x["score"])
        print(*(s["score"] for s in states))
        states = states[-int(round(len(states) * _TOP_PERCENTAGE)):]
        assert len(states) > 1
        new_states = []
        for _ in simulation_states:
            parents = [s["genome"] for s in states]
            parent1 = _get_random_element(parents)
            parent2 = _get_random_element(parents)

            nodes1, connections1 = parent1
            nodes2, connections2 = parent2

            # Get invoation numbers.
            inovation_numbers = sorted(list(
                set(c[3] for c in connections1) |
                set(c[3] for c in connections2)))

            # Index connections by inovation number.
            connections1 = {c[3]: c for c in connections1}
            connections2 = {c[3]: c for c in connections2}

            sections = groupby(
                [(connections1.get(i), connections2.get(i))
                    for i in inovation_numbers],
                lambda c:
                    None if c[0] and c[1] else (0 if c[0] is None else 1))
            connections = []
            for _, section in sections:
                connections.extend(c for c in choice(list(zip(*section))) if c)

            # TODO: keep only relevant nodes
            nodes = list(set(nodes1) | set(nodes2))

            new_states.append({"agent": {"genome": (nodes, connections)}})

        self._generations_count += 1
        return self._generations_count < _MAX_GENERATIONS, new_states
