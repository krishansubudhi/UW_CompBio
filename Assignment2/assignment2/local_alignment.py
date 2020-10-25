

class LocalAlignment:
    '''
    Args:
        scoring_matrix: dictionary of dictionaries which gives pairwise alignment scores
    '''
    def __init__(self, scoring_matrix:dict, gap_penalty ):
        self.scoring_matrix = scoring_matrix
        self.gap_penalty = gap_penalty
    
    def get_best_alignment(self, sequence1, sequence2):
        '''
        Args:
            sequence1, sequence2: Filename ending with .fasta or entire sequence string
        Returns:
            score : Best match score
            alignedpair : AlignedPair object with alignment information
            best_score_matrix : score matrix
        '''

        best_score_matrix= self.calculate_best_score_matrix(sequence1, sequence2)

        # best_score= np.max(best_score_matrix)
        # best_score_index = np.unravel_index(np.argmax(best_score_matrix), best_score_matrix.shape)

        best_score, aligned_pair = self.traceback(best_score_matrix, sequence1, sequence2)

        return aligned_pair, best_score, best_score_matrix

    def calculate_best_score_matrix(self, sequence1, sequence2):
        '''
        Calculates the scoring matrix using DP and local alignment algorithm
        '''
        matrix = np.zeros(len(sequence1)+1, len(sequence2)+1)
        
        for i in range(1, matrix.shape[0]):
            for j in range(1, matrix.shape[1]):
                matrix[i][j] = self._get_best_score(i, j , matrix)
        return matrix
    
    def traceback(self, best_score_matrix, sequence1, sequence2):
        

    def _get_best_score(self, i, j , matrix):
        return max(
            0,
            matrix[i-1][j-1] + self.scoring_matrix[i][j],
            matrix[i-1][j] + gap_penalty
            matrix[i][j-1] + gap_penalty
        )




