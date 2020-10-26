import numpy as np
class AlignedPair:
    '''
    Class to store two aligned sequences. Provides other utility functions too 
    Args:
        sequence1, sequence2: entire sequence string with gaps represented as '-'. Both sequences should be of same length.
    '''
    MAX_RES_IN_SINGLE_LINE = 60

    def __init__(self, 
                sequence1:str , 
                sequence2:str, 
                startpos1:int,
                startpos2:int):
        self.sequence1 = sequence1
        self.sequence2 = sequence2
        self.startpos1 = startpos1
        self.startpos2 = startpos2
        assert len(self.sequence1) == len(self.sequence2)

    def get_similarities(self, scoring_matrix:dict):
        return ''.join(
            [self._get_match_letter(c1,c2, scoring_matrix)
                for c1,c2 in zip(self.sequence1, self.sequence2)]
        )
    
    def _get_match_letter(self, c1, c2, scoring_matrix):
        if c1 == c2:
            return c1
        elif c1 == '-' or c2 == '-':
            return ' '
        elif scoring_matrix[c1][c2] > 0:
            return '+'
        else:
            return ' '
    
    def print_alignment(self, accession1, accession2, scoring_matrix:dict):
        '''
        * break them into blocks of 60 columns 
        * To the left of each row of the alignment, give the (1-based) index of the first letter in that row with respect to the sequence from which it was extracted
        * Leave a blank line between successive pairs of lines
        * replace in the blank middle line of each pair so as to highlight the similarities, as BLAST output does

        Example:
        P68871:  62  KAHGKKVLGAFSDGLAHLDN---LKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHH
                     +AH   V+ A ++ +  L +   ++ +   L E H  K     E F+ L  V++ VL   
        Q14SN0:  83  QAHCAGVITALNNVIDFLHDPGLMEASLIGLVERH-KKRGQTKEEFQNLKEVMLEVLRQA

        P68871: 119  FGKEFTPPVQAAYQKVV
                      GK++TP V  A+ K +      
        Q14SN0: 142  LGKQYTPEVAEAWNKTL
        
        where letters flag identities, and plus signs mark differences with positive BLOSUM 62 substitution scores.
        '''
        pos1 = self.startpos1
        pos2 = self.startpos2
        similarity = self.get_similarities( scoring_matrix)

        chunks = [(self.sequence1[i:i+60], self.sequence2[i:i+60], similarity[i:i+60]) for i in np.arange(0, len(self.sequence1), self.MAX_RES_IN_SINGLE_LINE)]

        for i in np.arange(0, len(self.sequence1), self.MAX_RES_IN_SINGLE_LINE):
            print()
            print('{:>6s}:{:4d}  {:60s}'.format(accession1, pos1, self.sequence1[i:i+60]))
            print('{:13s}{:60s}'.format(' ', similarity[i:i+60]))
            print('{:>6s}:{:4d}  {:60s}'.format(accession2, pos2, self.sequence2[i:i+60]))
            
            pos1 += len([res for res in self.sequence1[i:i+60] if res != '-'])
            pos2 += len([res for res in self.sequence2[i:i+60] if res != '-'])

        # https://docs.python.org/3/library/string.html#formatstrings

