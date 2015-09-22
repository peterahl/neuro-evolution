from .sim_object import SimObject
import numpy as np
#from scipy.special import expit
from ..position import directions, turn
from random import choice
from .empty import Empty
from .food import Food
from .wall import Wall
import itertools

np.set_printoptions(precision=2)

_OBJECT_TO_INPUT = {Wall.SYMBOL:(1,0,0), Empty.SYMBOL:(0,1,0), Food.SYMBOL:(0,0,1)}

_MAX_ENERGY = 1.0

_ENERGY_LEVELS = 5

#_NUMBER_OF_INPUTS = len(_OBJECT_TO_INPUT) * 3 + _ENERGY_LEVELS + 1  # fields front, left, right, energy level and last action ok
_NUMBER_OF_INPUTS = len(_OBJECT_TO_INPUT) * 3 # fields front, left, right, energy level and last action ok

_OUTPUT_INDEX_TO_ACTION = {
    0: SimObject.Action.MOVE, 
    1: SimObject.Action.EAT, 
    2: SimObject.Action.TURN_LEFT, 
    3: SimObject.Action.TURN_RIGHT,
    4: SimObject.Action.DO_NOTHING
}

def _connect_all_to_all(sources, targets, weight_matrix):
	""" Adds all to all connectivity for network between sources and targets
		with random values. row = target, col = source (to work with
		multiplication later"""	
	for s in sources:
		for t in targets:
			weight_matrix[t][s] = np.random.random()

def _max_index(input_vector):
    max_value = 0
    max_index = 0
    for i, element in enumerate(input_vector):
        if element > max_value:
            max_value = element
            max_index = i
    return max_index

def _energy_conversion(energy):
    energy_index = round(energy * (_ENERGY_LEVELS - 1) / _MAX_ENERGY)
    return [1 if i == index else 0 for i in range(_ENERGY_LEVELS)] 


class ANNSimpleAgent(SimObject):

    SYMBOL = "a"

    def __init__(self, n_inputs, n_outputs, n_layers = 3):
        self._n_layers = n_layers
        self._n_inputs = n_inputs
        self._n_middle = 4 #number of units in middle layer
        self._n_outputs = n_outputs
        self._n_nodes = self._n_inputs + self._n_middle + self._n_outputs
        self._node_values = np.array([0]*self._n_nodes) 
        self.set_random_weights_three_layer_network()       
        
        self._direction = choice(directions)
        self._action = None
        
        self._energy = _MAX_ENERGY
        self._binary_input = [0, ] * _NUMBER_OF_INPUTS

	
    def set_random_weights_three_layer_network(self):
        """ just something simple to create a weight matrix
			for a three layer network"""
			
        n_nodes = self._n_inputs + self._n_outputs + self._n_middle
        self._weights = np.zeros([n_nodes, n_nodes])
        nodes = list(range(n_nodes))
        layer1 = nodes[:self._n_inputs]
        layer2 = nodes[self._n_inputs:self._n_inputs+self._n_middle]
        layer3 = nodes[-self._n_outputs:]
		
        _connect_all_to_all(layer1, layer2, self._weights)
        _connect_all_to_all(layer2, layer3, self._weights)
        
        #print("--------WEIGHT MATRIX--------------")	
        #print(self._weights)

    def start_turn(self, objects_map):
        position = objects_map.get_position_for_object(self)
        front = objects_map.get_object_for_position(
            position.move(self._direction)).SYMBOL

        left = objects_map.get_object_for_position(
            position.move(turn(self._direction, False))).SYMBOL
        right = objects_map.get_object_for_position(
            position.move(turn(self._direction, True))).SYMBOL
        
        """create binary input vector"""
        """!right now ONLY what the agent 'sees', not 'effect of actions' or energy"""
        binary_input = [_OBJECT_TO_INPUT[f] for f in (front, left, right)]
        binary_input = list(itertools.chain.from_iterable(binary_input))      
       # print("binary input: ", binary_input)     
        self._set_inputs(binary_input) 
        
        """ Run network for as many steps as layers"""
        for i in range(self._n_layers-1):
            self._step()
                     
        """convert from binary to correct output format"""   
        output = self._get_outputs()   
        ind = _max_index(output)
        print("Max output index", ind)
        self._action = _OUTPUT_INDEX_TO_ACTION[ind]
		
    def _set_inputs(self, values):
        self._node_values[:self._n_inputs] = values
	
    def action(self):       
        return self._action
    
    def _step(self):
        self._node_values = np.dot(self._weights, self._node_values)
        #self._pretty_print_values(self._node_values)
   
    def _get_outputs(self):
        return self._node_values[-self._n_outputs:]
    
    def setweights(self, new_weights):
        self._weights = new_weights
    
    @property
    def direction(self):
        return self._direction

    def set_direction(self, direction):
        super().set_direction(direction)
        self._direction = direction
        
    def _pretty_print_values(self, values):
        """For debugging, hardcoded three layer network"""
        print('----------------------------')
        print("Input", str(values[:self._n_inputs]))
        print("Middle", values[self._n_inputs:-self._n_outputs])
        print("Output", values[-self._n_outputs:])
        print('----------------------------')

ANNSimpleAgent.register()


