
from assignment2.aligned_pair import AlignedPair
import numpy as np 

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

        best_score= np.max(best_score_matrix)
        aligned_pair = self.traceback(best_score_matrix, sequence1, sequence2)

        return aligned_pair, best_score, best_score_matrix

    def calculate_best_score_matrix(self, sequence1, sequence2):
        '''
        Calculates the scoring matrix using DP and local alignment algorithm
        '''
        matrix = np.zeros(shape = (len(sequence1)+1, len(sequence2)+1), dtype = int)
        
        for i in range(1, matrix.shape[0]):
            for j in range(1, matrix.shape[1]):
                matrix[i][j] = self._get_best_score(i, j , matrix, sequence1, sequence2)
        return matrix
    
    def traceback(self, best_score_matrix, sequence1, sequence2):
        '''
        Returns:
            best_score : Best alignment score
            aligned_pair : aligned pair object
        '''
        i,j = np.unravel_index(np.argmax(best_score_matrix), best_score_matrix.shape)

        aligned_seq_1 = []
        aligned_seq_2 = []

        matrix = best_score_matrix
        start_pos = (i,j)
        while True:
            if matrix[i][j] == 0:
                break
            else:
                start_pos = (i,j)
                if matrix[i-1][j-1] + self.scoring_matrix[sequence1[i-1]][sequence2[j-1]] == matrix[i][j]:
                    aligned_seq_1.insert(0, sequence1[i-1])
                    aligned_seq_2.insert(0, sequence2[j-1])
                    i,j = i-1, j-1
                elif matrix[i-1][j] + self.gap_penalty == matrix[i][j]:
                    aligned_seq_1.insert(0, sequence1[i-1])
                    aligned_seq_2.insert(0,'-')
                    i ,j = i-1, j
                elif matrix[i][j-1] + self.gap_penalty == matrix[i][j]:
                    aligned_seq_1.insert(0, '-')
                    aligned_seq_2.insert(0,sequence2[j-1])
                    i, j = i , j-1
                
        
        return AlignedPair(''.join(aligned_seq_1),''.join(aligned_seq_2), *start_pos)

    def _get_best_score(self, i, j , matrix, sequence1, sequence2):
        return max(
            0,
            matrix[i-1][j-1] + self.scoring_matrix[sequence1[i-1]][sequence2[j-1]],
            matrix[i-1][j] + self.gap_penalty,
            matrix[i][j-1] + self.gap_penalty
        )




