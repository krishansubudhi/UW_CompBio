import pandas as pd
import numpy as np
from collections import namedtuple

Vmax = namedtuple('Vmax_l','pb ptr') # max probability with back pointer at for a state in viterbi

class ViterbiInference:
    def __init__(self, emmisionP : pd.DataFrame, transitionP : pd.DataFrame, begin_state = 'B'):
        self.emmisionP_orig = emmisionP
        self.transitionP_orig = transitionP

        self.emmisionP = self.process_probability(emmisionP)
        self.transitionP = self.process_probability(transitionP)
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

    def get_viterbi_path(self, sequence):
        '''
        Given a sequence find the viterbi path for the state sequence
        '''
        # max probability at position 0 for all layers
        v_0 = {}
        v_0[self.begin_state] = Vmax(np.log(1), None)

        v_all = [v_0]
        for i,nt in enumerate(sequence):
            v = self.get_vmax(nt, v_all[-1])
            v_all.append(v)
        return v_all
    
    def get_vmax(self, nt ,v_prev):
        # logarithmic p so add
        v = {}
        prev_states = list(v_prev.keys())
        for end_state in self.states:
            vs = [ v_prev[begin_state].pb + self.get_transition_probability(begin_state, end_state) 
                    for begin_state in prev_states ]
            v[end_state] = Vmax(pb = np.max(vs) + self.get_emmision_probability(end_state, nt),
                                ptr = prev_states[np.argmax(vs)])
        return v

    def traceback(self, v_all):
        sorted_last = sorted(v_all[-1], key = lambda state: v_all[-1][state].pb, reverse = True) 
        path = []
        state = sorted_last[0]
        i = -1
        while state != self.begin_state:
            path.insert(0,state)
            state = v_all[i][state].ptr
            i -= 1
        return path

    def get_max_probability(self, v_all, position = -1):
        sorted_states = sorted(v_all[position], key = lambda state: v_all[position][state].pb, reverse = True) 
        return v_all[position][sorted_states[0]].pb

    def get_hits(self,path):
        path.insert(0,'Begin')
        path.append('End')
        #mark positions if state changes starts from 1
        positions = [(path[i], i) for i in range(1, len(path)) if path[i] != path[i-1]]
        hits = pd.DataFrame(positions, columns = ['state', 'start'])
        hits['end'] = hits['start'].shift(-1)-1
        hits = hits.drop(len(hits)-1)
        hits['end'] = hits['end'].astype(int)
        hits['length'] = hits['end']- hits['start']+1
        return hits

    def print(self, v_all, k = 10, hit_state = 'L'):
        '''
        the HMM emission/transition parameters used for this pass (e.g., from the tables above for pass 1),
        the log probability (natural log, base-e) of the overall Viterbi path,
        the total number of "hits" found, where a hit is (contiguous) subsequence assigned to state 2 in the Viterbi path, and
        the lengths and locations (starting and ending positions) of the first k (defined below) "hits." Print all hits, if there are fewer than k of them. (By convention, genomic positions are 1-based, not 0-based, indices.)
        '''
        print('Emission Probability')
        print(self.emmisionP_orig)

        print('\nTransition Probability')
        print(self.transitionP_orig)

        print('\nLog probability of viterbi path= ',self.get_max_probability(v_all).round(5))

        path = self.traceback(v_all)
        hits = self.get_hits(path)

        print('\nhits' )
        print(hits[hits.state == hit_state].head(k))