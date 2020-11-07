import pandas as pd
import numpy as np

# makeCountMatrix: build a count matrix corresponding to a given list of length k sequences.
# addPseudo: given a count matrix, and a pseudocount vector, build a new count matrix by adding them.
# makeFrequencyMatrix: make a frequency matrix from a count matrix.
# entropy: calculate the entropy of a frequency matrix relative to background.
# makeWMM: make a weight matrix from a frequency matrix and background vector. (It may be convenient to save the entropy with the WMM, too.)
# scanWMM: given a WMM of width k and one or more sequences of varying lengths ≥ k, scan/score each position of each sequence (excluding those < k from the rightmost end).

def makeCountMatrix(sequences : list):
    '''
    Given a list M containing n sequences, each of length k that are all presumed to be instances of one motif, the count matrix representing it is a 4 by k table whose i, j entry (1 ≤ i ≤ 4, 1 ≤ j ≤ k) is the count of the number of times nucleotide i appears in position j in a string in M. Again, rows 1, 2, 3, 4 should correspond to nucleotides A, C, G, T in that order. Note that each column of such count table should sum to the same number; before pseudocounting, this number will be n, the number of sequences in M; after pseudocounting, it will be n+p, where p is the sum of the pseudocount vector.
    
    Args:
        sequences : list of sequences each of length k (all are instances of one motif)
    Returns:
        pandas count matrix with neucleotytes as index, position as columns
    Example:
        ACCGT
        TACGG

        matrix : 
            1   2   3   4   5
        A   1   1   0   0   0
        C   0   1   2   0   0
        G   0   0   0   2   1
        T   1   0   0   0   1
    '''
    sequences = np.array(sequences)
    s = [list(seq) for seq in sequences]
    s = np.array(s)

    motif_length = s.shape[1]
    cm = pd.DataFrame(np.zeros((4, motif_length)), 
                        index = ['A','C','G','T'], 
                        columns = range(1, motif_length +1),
                        dtype = int
                    )
    
    for nt in 'ACGT':
        cm.loc[nt] = (s == nt).sum(axis=0)
    return cm


def addPseudo(cm: pd.DataFrame, pseudocount : list):
    '''
    given a count matrix, and a pseudocount vector, build a new count matrix by adding them
    Args:
        pseudocount:  pseudocount vector is also a length 4 vector of non-negative reals (with unconstrained sum), again ordered A, C, G, T.
    '''
    return cm + np.array(pseudocount).reshape(-1,1)


