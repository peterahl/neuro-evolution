from .sim_object import SimObject
import numpy as np
from scipy.special import expit
from ..position import directions, turn
from random import choice
from .empty import Empty
from .food import Food


class ANNSimpleAgent(SimObject):

    SYMBOL = "s"

    def __init__(self, weights, n_inputs, n_outputs = 5, n_layers = 4):
        self._weights = np.array()
        self._n_nodes = len(weights)
        self._n_layers = n_layers
        
        self._node_values = np.zeros(self._n_nodes, 1)
        self._n_inputs = n_inputs
        self._n_outputs = n_outputs
        
        self._direction = choice(directions)
        self._action 
        
        self._input_dict = {'#':(1,0,0), ' ':(0,1,0), '*':(0,0,1)}
        self._action_dict = {0:self.Action.MOVE, 
                             1:self.Action.EAT, 
                             2:self.Action.TURN_LEFT, 
                             3:self.Action.TURN_RIGHT,
                             4:self.Action.DO_NOTHING}
    

    def start_turn(self, objects_map):
        
        position = objects_map.get_position_for_object(self)
        front = objects_map.get_object_for_position(
            position.move(self._direction))

        left = objects_map.get_object_for_position(
            position.move(turn(self._direction, False)))
        right = objects_map.get_object_for_position(
            position.move(turn(self._direction, True)))
        visible = (front, left, right)
        n_input_attributes = len(visible)
        n_values_per_attribute = 3
        
        """create binary input vector"""
        binary_input = [0,]*n_input_attributes*n_values_per_attribute
        
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
    
    def step(self):
        """ do somthing with the sigmoid function """
        self._node_values = np.dot(self.weights, self._node_values)        
    
    def set_inputs(self, values):
        self.node_values[0:self.n_inputs-1] = values
    
    def get_outputs(self):
        return self.node_values[-self.n_outputs:]
    
    def setweights(self, weights):
        pass
    
    @property
    def direction(self):
        return self._direction

    def set_direction(self, direction):
        super().set_direction(direction)
        self._direction = direction
