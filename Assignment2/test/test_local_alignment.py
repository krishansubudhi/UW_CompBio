import unittest
from assignment2.local_alignment import LocalAlignment
import pandas as pd
import numpy as np

class TestLocalAlignment(unittest.TestCase):

    def test_alignment(self):
        '''
            A B
            C D
        A-C = 10
        A-D = -2
        B-D = 30
        B-C = 15
        gap_penanlty = -1

        Score matrix = 

        0 0                         0
        0 10                        max(0-2, 10-1 -1, 0)
        0 max(15+0,10-1,0-1,0)      max(30+10, 15-1, 9-1,0)
        '''

        scoring_matrix = {
            'A':{'C':10, 'D':-2},
            'B':{'C':15, 'D':30}
        }
        gap_penalty = -1

        la = LocalAlignment(scoring_matrix, gap_penalty)
        matrix = la.calculate_best_score_matrix('AB','CD')
        expected = np.array([
            [ 0,0 ,0], 
            [ 0,10,9],
            [ 0,15,40]])
        assert (matrix == expected).all()

        #traceback
        pair = la.traceback( matrix, 'AB','CD')
        assert pair.sequence1 == list('AB')
        assert pair.sequence2 == list('CD')

        pair, best_score, best_score_matrix = la.get_best_alignment( 'AB','CD')
        assert pair.sequence1 == list('AB')
        assert pair.sequence2 == list('CD')
        assert best_score == 40
        assert (best_score_matrix == expected).all()