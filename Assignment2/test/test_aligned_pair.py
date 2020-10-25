import unittest
from assignment2.aligned_pair import AlignedPair
from assignment2.score import get_score_matrix


score_matrix = get_score_matrix('blosum62.txt')

class TestAlignedPair(unittest.TestCase):
    def test_get_similarities(self):
        pair = AlignedPair('KAHGKKVLGAFSDGLAHLDN---LKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHH',
         'QAHCAGVITALNNVIDFLHDPGLMEASLIGLVERH-KKRGQTKEEFQNLKEVMLEVLRQA',
         62, 83)
        sim = pair.get_similarities(score_matrix)

        assert sim == '+AH   V+ A ++ +  L +   ++ +   L E H  K     E F+ L  V++ VL   '
    def test_print_alignment(self):
        pair = AlignedPair('KAHGKKVLGAFSDGLAHLDN---LKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVV',
         'QAHCAGVITALNNVIDFLHDPGLMEASLIGLVERH-KKRGQTKEEFQNLKEVMLEVLRQALGKQYTPEVAEAWNKTL',
         62, 83)
        pair.print_alignment('P68871','Q14SN0',score_matrix)
