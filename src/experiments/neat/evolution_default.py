# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import count
from random import random, choice

from ne_simulator.evolution import Evolution
from ne_simulator.sim_objects.neat_agent import _INPUT_NUMBER, Node, Connection
from ne_simulator.sim_objects.neat_agent import _OUTPUT_NUMBER
from ne_simulator.sim_objects.neat_agent import NodeType


_RANDOM_CONNECTION_PROB = 0.8

node_id_seq = count()

_innovation_id_seq = count()

innovations = defaultdict(lambda: next(_innovation_id_seq))


def random_weight():
    return choice([1, -1]) * random()


class Evolution(Evolution):

    def __init__(
            self, scenarios, simulators_count, wait_for_enter=False,
            multiprocessing=False, **kwds):
        super().__init__(
            scenarios, simulators_count, wait_for_enter, multiprocessing,
            **kwds)

        in_nodes = [
            Node(next(node_id_seq), NodeType.INPUT)
            for _ in range(_INPUT_NUMBER)]
        out_nodes = [
            Node(next(node_id_seq), NodeType.OUTPUT)
            for _ in range(_OUTPUT_NUMBER)]
        for simulation_state in self._simulation_states:
            connections = []

            for node, _ in in_nodes:
                connection_prob = random()

                if connection_prob > _RANDOM_CONNECTION_PROB:
                    out_node, _ = choice(out_nodes)
                    connections.append(
                        Connection(
                            node, out_node, random_weight(),
                            innovations[(node, out_node)], True))
            simulation_state["agent"] = {}
            simulation_state["agent"]["genome"] = (
                in_nodes + out_nodes, connections)
            # print(agent["genome"])
