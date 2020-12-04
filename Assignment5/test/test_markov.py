import unittest
from assignment5.markov import MarkovModel, GeneModel
import math
class TestMarkovModel(unittest.TestCase):
    def setUp(self):
        self.markov = MarkovModel(k = 3, pseudo_count=0)
        self.markov.build(['ATCG'])

    def test_create_counts(self):
        c, c1 = self.markov.create_counts(['ATCG', 'ATC']) #ignore ATC since it's less than 3+1 length
        assert c['ATC'] == 1
        assert c['TCG'] == 1
        assert c1['ATCG'] == 1
        print(c, c1)

    def test_getprobability(self):
        assert self.markov.get_probability('ATC') == 0.5
        #Conditional P(G|ATC)
        assert self.markov.get_probability('ATCG') == 1
        assert self.markov.get_probability('ATCT') == 0
        assert self.markov.get_probability('TTT') == 0

        self.markov.pseudo_count = 1
        assert self.markov.get_probability('ATCG') == 2/5
        assert self.markov.get_probability('ATCT') == 1/5
        assert self.markov.get_probability('TTT') == 0
    
    def test_getlogp(self): 
        assert self.markov.get_log_p('ATCG') == 0
        assert self.markov.get_log_p('ATC') == math.log(0.5)
        self.assertRaises(AssertionError, self.markov.get_log_p, 'ATCT')
    
    def test_get_logll(self):
        self.markov.pseudo_count = 1
        ll = self.markov.get_loglikelihood('ATCGC')
        assert ll == (self.markov.get_log_p('ATC')
                    + self.markov.get_log_p('ATCG')
                    + self.markov.get_log_p('TCGC'))


class TestGeneModel(unittest.TestCase):
    def test_llratio(self):
        model = GeneModel(k=3, pseudo_count=1)
        model.build(['ATCG'], ['TATCA'])
        assert model.foreground.get_probability('ATCG') == 2/5

        ll_ratio =  model.get_loglikelihood_ratio('ATCG')
        assert ll_ratio == math.log (
            (model.foreground.get_probability('ATC') * model.foreground.get_probability('ATCG')) / (model.background.get_probability('ATC') * model.background.get_probability('ATCG'))
        )
