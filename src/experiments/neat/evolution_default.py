# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import count
from random import random, choice

from ne_simulator.evolution import Evolution
from ne_simulator.sim_objects.neat_agent import _INPUT_NUMBER
from ne_simulator.sim_objects.neat_agent import _OUTPUT_NUMBER
from ne_simulator.sim_objects.neat_agent import NodeType


_RANDOM_CONNECTION_PROB = 0.8

_node_id_seq = count()

_inovation_id_seq = count()

_inovations = defaultdict(lambda: next(_inovation_id_seq))


class Evolution(Evolution):

    def __init__(
            self, scenarios, simulators_count, wait_for_enter=False,
            multiprocessing=False, **kwds):
        super().__init__(
            scenarios, simulators_count, wait_for_enter, multiprocessing,
            **kwds)

        in_nodes = [
            (next(_node_id_seq), NodeType.INPUT)
            for _ in range(_INPUT_NUMBER)]
        out_nodes = [
            (next(_node_id_seq), NodeType.OUTPUT)
            for _ in range(_OUTPUT_NUMBER)]

        for agent in self._simulation_states:
            connections = []

            for node, _ in in_nodes:
                connection_prob = random()

                if connection_prob > _RANDOM_CONNECTION_PROB:
                    out_node, _ = choice(out_nodes)
                    weight = choice([1, -1]) * random()
                    connections.append(
                        (node, out_node, weight, _inovations[(node, out_node)])
                    )
            agent["genome"] = (in_nodes + out_nodes, connections)
            # print(agent["genome"])
