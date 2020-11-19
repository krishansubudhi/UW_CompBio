from .viterbi import ViterbiInference
import pandas as pd
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
        return viterbi.get_hits(path)

    def maximization(self):
        pass

    def em_step(self):
        hits = self.expectation()
        
        