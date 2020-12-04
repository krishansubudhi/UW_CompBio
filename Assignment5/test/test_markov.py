import unittest
from assignment5.markov import MarkovModel
class TestMarkovModel(unittest.TestCase):
    def setUp(self):
        self.markov = MarkovModel(k = 3, pseudo_count=0)
    def test_create_counts(self):
        c = self.markov.create_counts(['ATCG', 'ATC']) #ignore ATC since it's less than 3+1 length
        assert c['ATC'] == 1
        assert c['TCG'] == 1
        assert c['ATCG'] == 1
        print(c)
