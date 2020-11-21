from unittest import TestCase
from unittest.mock import MagicMock
from assignment4.train import *

class TestTrain(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        print('Init called') #called before every function
    
    @classmethod
    def setUpClass(self):
        #called once at the beginning
        self.emmisionP = pd.DataFrame([ [1/6]*6, 
                                  [1/10]*5+[1/2] ], 
                                  index = ['F','L'], columns = range(1,7))
        self.transitionP = pd.DataFrame([[0.52,0.48],
                                    [0.6,0.4], 
                                    [0.17, 0.83]], 
                                    columns = ['L','F'], index = ['B','L','F'])
        self.sequence = [3,1,6,6,6,4]
        self.trainer = ViterbiTrain(self.sequence, self.emmisionP, self.transitionP, 'B')
        print('setUpClass called')

    def setUp(self):
        print('Set up called') # called before every function
    
    def test_sanity(self):
        assert (self.trainer.emmisionP == self.emmisionP).all().all()

    def test_expectation(self):
        path, v_all = self.trainer.expectation()
        assert path == ['F', 'F', 'L', 'L', 'L', 'F']

    def test_calculateFrequencies(self):
        path = ['F', 'F', 'L', 'L', 'L', 'F']
        #self.sequence = [3,1,6,6,6,4]
        ef, tf = self.trainer.calculateFrequencies(path)
        print(ef)
        print(tf)
        assert ef.loc['F'][6] == 0
        assert tf.loc['F']['L'] == 1
    
    def test_updateTransitionP(self):
        tf = pd.DataFrame([ [0,0],
                            [2,1],
                            [1,1]
                        ], index = list('BLF'), columns = list('LF'))
        self.trainer.updateTransitionP(tf)
        print(self.trainer.transitionP)
        truth = np.array(self.trainer.transitionP.values == [
                                                [0.52, 0.48 ],
                                                [2/3,1/3],
                                                [0.5,0.5]
                                            ])
        # print(truth, truth.all())
        assert truth.all()

    def test_updateEmissionP(self):
        ef = pd.DataFrame([ [1]*6,
                            [1]*5+[2]
                        ], index = ['F','L'], columns = range(1,7))
        self.trainer.updateEmissionP(ef)
        print(self.trainer.emmisionP)
        # truth = np.array(self.trainer.transitionP.values == [
        #                                         [1/6]*6,
        #                                         [1/7]*5+[2/7]
        #                                     ])
        # print(truth, truth.all()) #rounding error
        assert self.trainer.emmisionP.loc['F'].sum().round() == 1
        assert self.trainer.emmisionP.loc['L'].sum().round() == 1
        assert (self.trainer.emmisionP.loc['L'][6]/self.trainer.emmisionP.loc['F'][6]).round() == 2

    def test_maximization(self):
        path = ['F', 'F', 'L', 'L', 'L', 'F']
        #self.sequence = [3,1,6,6,6,4]
        self.trainer.maximization(path)
        print(self.trainer.emmisionP)
        print(self.trainer.transitionP)
        
        assert self.trainer.emmisionP.loc['L'][6] == 1
        assert self.trainer.transitionP.loc['L']['F'] == 1/3

    def test_em_step(self):
        total_iter = 3
        self.trainer.pseudo_count = 0.01
        for i in range(total_iter + 1):
            print(f'\nIteration {i}')
            path, v_all = self.trainer.expectation()
            self.trainer.viterbi.print(v_all)
            if i < total_iter:
                self.trainer.maximization(path)