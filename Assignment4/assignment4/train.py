from .viterbi import ViterbiInference
import pandas as pd
import numpy as np
import collections
class ViterbiTrain:
    def __init__(self, sequence , emmisionP : pd.DataFrame, transitionP : pd.DataFrame, begin_state = 'B' ):
        self.emmisionP = emmisionP
        self.transitionP = transitionP
        self.begin_state = begin_state
        self.states = [key for key in transitionP.keys() if key !=self.begin_state]
        self.sequence = sequence
        self.pseudo_count = 0 # change to 0.00001 if log(0) is encountered 
    
    def expectation(self):
        self.viterbi = ViterbiInference(self.emmisionP, self.transitionP, self.begin_state)
        v_all = self.viterbi.get_viterbi_path(self.sequence)
        path = self.viterbi.traceback(v_all)
        return path

    def maximization(self, path):
        #Emission
        ef, tf = self.calculateFrequencies(path)
        ef += self.pseudo_count
        tf += self.pseudo_count
        self.updateTransitionP(tf)
        self.updateEmissionP(ef)


    def em_step(self):
        path = self.expectation()
        maximization(path)
    
    def updateTransitionP(self, tf):
        #calculate probability
        p = tf.multiply(1/tf.sum(axis = 1), axis = 0)
        #Use original begin state
        p.loc[self.begin_state] = self.transitionP.loc[self.begin_state]
        self.transitionP = p
    
    def updateEmissionP(self, ef):
        p = ef.multiply(1/ef.sum(axis = 1), axis = 0)
        self.emmisionP = p

    def calculateFrequencies(self, path):
        emission = (self.emmisionP * 0).astype(int) #{state: collections.defaultdict(int) for state in self.states}
        transition = (self.transitionP * 0).astype(int) #{state: collections.defaultdict(int) for state in self.states}
        assert len(self.sequence) == len(path)
        prev_state = None
        for nt, state in zip(self.sequence, path):
            emission.loc[state][nt] += 1
            if prev_state:
                transition.loc[prev_state][state] += 1
            prev_state = state

        return emission, transition
        # return df.multiply(1/df.sum(axis = 1), axis = 0)
    