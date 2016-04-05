#!/usr/bin/python3
import uuid
import pygraphviz as PG
import random

A = PG.AGraph(directed=True, strict=True)

class Dot(object):

    def dot_tree(self):
        if self.node_type != 'Network':
            for child in self.children:
                A.add_edge(self.dot_name, child.dot_name)
                child.dot_tree()

class CreateChildren(object):

    def add_child(self, dna_chunk, network):
        if len(dna_chunk) == 1:
            self.children.append(Network(dna_chunk[0], self))
        elif dna_chunk[0] == '0':
            self.add_child(dna_chunk[1:], network)
        else:
            name = dna_chunk[0]
            if name not in [node.name for node in self.children]:
                self.children.append(Node(name, self))
            for node in self.children:
                if node.name == name:
                    node.add_child(dna_chunk[1:], network)
                    break

    def get_parent_name(self):
        if self.name == 'Root':
            return ''
        elif self.parent.name == 'Root':
            return self.name
        else:
            return self.parent.get_parent_name() + self.name

class Root(CreateChildren, Dot):

    MAX_DEAPTH = 4

    def __init__(self, dna):
        self.dna = dna
        self.name = 'Root'
        self.dot_name = 'Root'
        self.node_type = 'Root'
        self.children = list()

        for i in range(0, len(dna), self.MAX_DEAPTH):
            dna_chunk = dna[i:i+self.MAX_DEAPTH]
            network = dna[self.MAX_DEAPTH]
            if int(dna_chunk) == 0:
                pass
            else:
                self.add_child(dna_chunk, network)

class Node(CreateChildren, Dot):

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.dot_name = 'Node ' + self.get_parent_name()
        self.node_type = 'Node'
        self.children = list()

class Network(Dot):

    def __init__(self, name, parent):
        uid = str(uuid.uuid4())[:4]
        self.name = name
        self.dot_name = 'Net-{} type-{}'.format(uid, name)
        self.parent = parent
        self.node_type = 'Network'


dna = '123 4 124 5 001 2 002 1'
dna='1239124500120011'

# dna = ['1204',
#        '1205',
#        '0006',
#        '0006',
#        '0006',
#        '0006',
#        '0012',
#        '0021',
# ]

# dna = ''.join(dna)
# dna = ''.join([str(random.randint(0,5)) for n in range(80)])


test_node = Root(dna)
test_node.dot_tree()

# A.layout(prog='circo')
A.layout(prog='dot')
A.draw('tree.png')
