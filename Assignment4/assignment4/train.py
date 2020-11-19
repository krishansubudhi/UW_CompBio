from .viterbi import ViterbiInference
import pandas as pd
import collections
class ViterbiTrain:
    def __init__(self, sequence , emmisionP : pd.DataFrame, transitionP : pd.DataFrame, begin_state = 'B' ):
        self.emmisionP = emmisionP
        self.transitionP = transitionP
        self.begin_state = begin_state
        self.states = [key for key in transitionP.keys() if key !=self.begin_state]
        self.sequence = sequence
    
    def expectation(self):
        viterbi = ViterbiInference(self.emmisionP, self.transitionP, self.begin_state)
        v_all = viterbi.get_viterbi_path(self.sequence)
        path = viterbi.traceback(v_all)
        return path

    def maximization(self, path, hits):
        #Emission
        ef, tf = self.calculateFrequencies(path)

    def em_step(self):
        path = self.expectation()
        maximization(path)
    
    def calculateFrequencies(self, path):
        emission = {state: collections.defaultdict(int) for state in self.states}
        transition = {state: collections.defaultdict(int) for state in self.states}
        assert len(self.sequence) == len(path)
        prev_state = None
        for nt, state in zip(self.sequence, path):
            emission[state][nt] += 1
            if prev_state:
                transition[prev_state][state] += 1

        return pd.DataFrame(emission).T, pd.DataFrame(transition).T
        # return df.multiply(1/df.sum(axis = 1), axis = 0)
    