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
        raise NotImplementedError()
    
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

        chunks = [(self.sequence1[i:i+60], self.sequence2[i:i+60]) for i in np.arange(0, len(self.sequence1), self.MAX_RES_IN_SINGLE_LINE)]

        # https://docs.python.org/3/library/string.html#formatstrings

        def chunk_alignment_str(chunk):
            return '''{:>6s}:{:4d}  {:60s}
                    {:13s}{:60s}
                    {:>6s}:{:4d}  {:60s}'''\
                    .format(
                        accession1, pos1, chunk[0],
                        ' ',self.get_similarities(chunk[0], chunk[1]),
                        accession2, pos2, chunk[1],
                    )

        for chunk in chunks:
            print(chunk_alignment_str(chunk))
            print()
            pos1 += len([res for res in chunk[0] if res != '-'])
            pos2 += len([res for res in chunk[1] if res != '-'])


