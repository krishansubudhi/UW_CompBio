import pandas as pd
import numpy as np
from collections import namedtuple

Vmax = namedtuple('Vmax_l','pb ptr') # max probability with back pointer at for a state in viterbi

class ViterbiInference:
    def __init__(self, emmisionP, transitionP, begin_state = 'B'):
        self.emmisionP = process_probability(emmisionP)
        self.transitionP = process_probability(transitionP)
        self.begin_state = begin_state
        self.states = [key for key in transitionP.keys() if key !=self.begin_state]
    
    def process_probability(self, df):
        '''
        calculate log probability and return a dictionary for faster computation
            A    B
        1  0.1  0.9
        2  0.2  0.8

        becomes 

        {1: {'A': -2.3025, 'B': -0.1053},
         2: {'A': -1.6094, 'B': -0.2231}}
        '''
        return np.log(df).T.to_dict()

    def get_emmision_probability(self, state, value):
        return self.emmisionP[state][value]
    def get_transition_probability(self, state1, state2):
        return self.transitionP[state1][state2]

    def get_viterbi_path(sequence):
        '''
        Given a sequence find the viterbi path for the state sequence
        '''
        # max probability at position 0 for all layers
        v_0 = {state: Vmax(0, None) for state in self.states}
        v_0[self.begin_state] = 1

        v_all = [v_0]
        for i,nt in enumerate(sequence):
            v = self.get_vmax(nt, v_all[-1])
            v_all.append(v)
        return v_all
    
    def get_vmax(self, nt ,v_prev):
        # logarithmic p so add
        v = {}
        prev_states = v_prev.keys()
        for end_state in self.states:
            vs = [ v_prev[begin_state] * self.get_transition_probability(begin_state, end_state) 
                    for begin_state in prev_states ]
            v[end_state] = Vmax(pb = np.max(vs)* self.get_emmision_probability(end_state, nt),
                                ptr = prev_states[np.argmax[vs]])
        return v

