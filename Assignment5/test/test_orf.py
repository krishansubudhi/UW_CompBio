from assignment5.orf import *
import unittest
class TestORFFinder(unittest.TestCase):
    def setUp(self):
        self.sequence = 'TAAGCTAGCGCTGA'
    def test_get_all_orfs(self):
        finder = ORFFinder()
        df = finder.get_all_orfs(self.sequence)
        assert len(df) == 1
        print(df)

        # df = finder.get_all_orfs(self.sequence,readingframe= 2)
        # assert len(df) == 1

        df = finder.get_all_orfs(self.sequence,readingframe= 3)
        assert len(df) == 2
        assert df.loc[0].start == 3
        assert df.loc[0].end == 5 # TAG
        print(df)