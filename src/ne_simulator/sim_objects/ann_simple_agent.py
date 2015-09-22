from .sim_object import SimObject
import numpy as np
from scipy.special import expit
from ..position import directions, turn
from random import choice
from .empty import Empty
from .food import Food


_OBJECT_TO_INPUT = {Wall.SYMBOL:(1,0,0), Empty.SYMBOL:(0,1,0), Food.SYMBOL:(0,0,1)}

_MAX_ENERGY = 1.0

_ENERGY_LEVELS = 5

_NUMBER_OF_INPUTS = len(_OBJECT_TO_INPUT) * 3 + _ENERGY_LEVELS + 1  # fields front, left, right, energy level and last action ok

_OUTPUT_INDEX_TO_ACTION = {
    0: SimObject.Action.MOVE, 
    1: SimObject.Action.EAT, 
    2: SimObject.Action.TURN_LEFT, 
    3: SimObject.Action.TURN_RIGHT,
    4: SimObject.Action.DO_NOTHING
}


def _max_index(input_vector):
    max_value = 0
    max_index = 0
    for i, element in enumerate(input_vector):
        if element > max_value:
            max_value = element
            max_index = i
    return max_index

def _energy_conversion(energy):
    eneryg_index = round(energy * (_ENERGY_LEVELS - 1) / _MAX_ENERGY)
    return [1 if i == index else 0 for i in range(_ENERGY_LEVELS)] 


class ANNSimpleAgent(SimObject):

    SYMBOL = "s"

    def __init__(self, weights, n_layers = 4):
        self._weights = np.array()
        self._n_nodes = len(weights)
        self._n_layers = n_layers
        
        self._node_values = np.zeros(self._n_nodes, 1)
        self._n_inputs = n_inputs
        self._n_outputs = n_outputs
        
        self._direction = choice(directions)
        self._action 
        
        self._energy = _MAX_ENERGY
        self._binary_input = [0, ] * _NUMBER_OF_INPUTS


    def start_turn(self, objects_map):
        
        position = objects_map.get_position_for_object(self)
        front = objects_map.get_object_for_position(
            position.move(self._direction))

        left = objects_map.get_object_for_position(
            position.move(turn(self._direction, False)))
        right = objects_map.get_object_for_position(
            position.move(turn(self._direction, True)))
        # visible = (front, left, right)
        # n_input_attributes = len(visible)
        # n_values_per_attribute = 3
        
        """create binary input vector"""
        binary_input = [_OBJECT_TO_INPUT[f] for f in (front, left, right)]
        binary_input.append(self._energy)
        

        for i in range(0,len(visible)):
            binary_input[i*3:(i+1)*3] = self._input_dict[visible[i]]
           
        self._set_inputs(binary_input) 
        
        """ Run network for as many steps as layers """
        for i in range(self._n_layers):
            self.step()
                     
        """convert from binary to correct output format"""   
        output = self.get_outputs()        
        ind = output.index(max(output))
        self._action = self._action_dict[ind]


    def action(self):       
        return self._action
    
    def _step(self):
        self._node_values = expit(np.dot(self.weights, self._input_values + self._node_values))
    
    def _get_outputs(self):
        return self.node_values[-self.n_outputs:]
    
    def setweights(self, weights):
        pass
    
    @property
    def direction(self):
        return self._direction

    def set_direction(self, direction):
        super().set_direction(direction)
        self._direction = direction
