# -*- coding: utf-8 -*-
from itertools import groupby, chain
from random import randrange, choice, random

from ne_simulator.sim_objects.neat_agent import NodeType, Connection, Node

from .evolution_default import Evolution as DefaultEvolution, innovations, \
    node_id_seq, random_weight

_TOP_PERCENTAGE = 0.40

_WEIGHT_MUTATION_PROBABILITY = 0.15

_WEIGHT_SCALE_FACTOR = 0.15

_WEIGHT_REPLACEMENT_PROBABILITY = 0.05

_ADD_CONNECTION_PROBABILITY = 0.10

_ADD_NODE_PROBABILITY = 0.10

_DISABLE_PROBABILITY = 0.05

_ENABLE_PROBABILITY = 0.05

_NOT_MUTATE_PROBABILITY = 0.1

_CROSS_PROBABILITY = 0.9


def _get_random_elements(values, count):
    return tuple(
        values.pop(randrange(0, len(values))) for _ in range(count))


def _cleanup_nodes(nodes, connections):
    hidden_nodes = set(n.id for n in nodes if n.node_type == NodeType.HIDDEN)
    hidden_nodes -= set(
        chain.from_iterable((c.node_in, c.node_out) for c in connections))
    return [n for n in nodes if n.id not in hidden_nodes]
    # return hidden_nodes & set(
    #     chain.from_iterable(*[(c.node_in, c.node_out) for c in connections]


def _cross_genome(parents):
    parent1, parent2 = _get_random_elements(parents, 2)

    nodes1, connections1 = parent1
    nodes2, connections2 = parent2

    if random() > _CROSS_PROBABILITY:
        if random() < 0.5:
            return list(nodes1), list(connections1)
        else:
            return list(nodes2), list(connections2)

    # Get invoation numbers.
    innovation_numbers = sorted(list(
        set(c.innovation for c in connections1) |
        set(c.innovation for c in connections2)))

    # Index connections by inovation number.
    connections1 = {c.innovation: c for c in connections1}
    connections2 = {c.innovation: c for c in connections2}

    sections = groupby(
        [(connections1.get(i), connections2.get(i))
            for i in innovation_numbers],
        lambda c: None if c[0] and c[1] else (0 if c[0] is None else 1))
    connections = []
    for _, section in sections:
        connections.extend(c for c in choice(list(zip(*section))) if c)

    nodes = list(set(nodes1) | set(nodes2))

    # return _cleanup_nodes(nodes, connections), connections
    return nodes, connections


def _mutate_weights(connections):
    # Mutate weights.
    for (i, c) in enumerate(connections):
        weight = c.weight  # shortcut
        # Mutation
        weight += (
            (random_weight() * _WEIGHT_SCALE_FACTOR)
            if random() < _WEIGHT_MUTATION_PROBABILITY
            else 0)
        if weight > 1:
            weight = 1.0
        if weight < -1:
            weight = -1.0
        # Replacement
        weight = (
            random_weight()
            if random() < _WEIGHT_REPLACEMENT_PROBABILITY
            else weight)
        connections[i] = Connection(
            c.node_in, c.node_out, weight, c.innovation, c.enabled)


def _add_connection(nodes, connections):
    # Add connection.
    if random() < _ADD_CONNECTION_PROBABILITY:
        (node1_id, _), (node2_id, _) = _get_random_elements(list(nodes), 2)
        connections.append(
            Connection(
                node1_id, node2_id, random_weight(),
                innovations[(node1_id, node2_id)], True))


def _add_node(nodes, connections):
    if connections and random() < _ADD_NODE_PROBABILITY:
        # Get connection to replace.
        connection_index = randrange(0, len(connections))
        connection = connections[connection_index]
        # Create new node.
        new_node = next(node_id_seq)
        nodes.append(Node(new_node, NodeType.HIDDEN))
        # Add new connections.
        connections.append(
            Connection(
                connection.node_in, new_node, 1,
                innovations[(connection.node_in, new_node)], True))
        connections.append(
            Connection(
                new_node, connection.node_out, connection.weight,
                innovations[(new_node, connection.node_out)], True))
        # Disable replaced connection.
        connections[connection_index] = Connection(
            connection.node_in, connection.node_out, connection.weight,
            connection.innovation, False)


def _flip_connection_status(connections, index):
    c = connections[index]
    connections[index] = Connection(
        c.node_in, c.node_out, c.weight, c.innovation, not c.enabled)


def _enable_disable_connections(connections):
    if not connections:
        return
    states = [
        (i if c.enabled else None, i if not c.enabled else None)
        for i, c in enumerate(connections)]
    enabled, disabled = zip(*states)

    enabled = [i for i in enabled if i is not None]
    if enabled and random() < _DISABLE_PROBABILITY:
        _flip_connection_status(connections, choice(enabled))
    disabled = [i for i in disabled if i is not None]
    if disabled and random() < _ENABLE_PROBABILITY:
        _flip_connection_status(connections, choice(disabled))


class Evolution(DefaultEvolution):

    def __init__(self, *args, **kwds):
        kwds["multiprocessing"] = True
        super().__init__(*args, **kwds)
        self._generations_count = 0
        self._max_generations = kwds["max_generations"]

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
            nodes, connections = _cross_genome([s["genome"] for s in states])
            if random() > _NOT_MUTATE_PROBABILITY:
                _mutate_weights(connections)
                _enable_disable_connections(connections)
                _add_connection(nodes, connections)
                _add_node(nodes, connections)

            new_states.append({"agent": {"genome": (nodes, connections)}})

        self._generations_count += 1
        return self._generations_count < self._max_generations, new_states
