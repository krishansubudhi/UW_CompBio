

class LocalAlignment:
    '''
    Args:
        scoring_matrix: dictionary of dictionaries which gives pairwise alignment scores
    '''
    def __init__(self, scoring_matrix:dict):
        self.scoring_matrix = scoring_matrix
    
    def get_best_alignment(self, sequence1, sequence2):
        '''
        Args:
            sequence1, sequence2: Filename ending with .fasta or entire sequence string
        Returns:
            score : Best match score
            alignedpair : AlignedPair object with alignment information
        '''

