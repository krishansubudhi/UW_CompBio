import pandas as pd
import numpy as np
from .build_matrices import *

def Estep(wmm, sequences, background = [0.25, 0.25, 0.25, 0.25]):
    '''
    what is E[zij], where zij is the zero-one variable indicating 
    whether the motif instance in sequence i begins in position j.
    (scanWMM does most of the required work.)
    '''
    # return np.array([calculate_Ej(wmm, seq) for seq in sequences]) #loops for i dimension
    probs = calculateProbabilities(wmm, background)
    E_zij = np.array([Estep_single(probs, seq) for seq in sequences])
    return E_zij

def Estep_single(probs, sequence):
    def calculate_expectation(probs , possible_motif):
        return np.product(probs.lookup(list(possible_motif),probs.columns))
    motif_len = probs.shape[1]
    E_i = []
    for j in range(0, len(sequence) - motif_len + 1):
        E_j = calculate_expectation(probs, sequence[j:j + motif_len])
        E_i.append(E_j)
    E_i = np.array(E_i)
    # normalize
    return E_i / E_i.sum()

def Mstep(E_zij, sequences, k = 10, pseudocount : list, background : list):
    assert E_zij.shape[1] == len(sequences[0])-k+1
    kmers = []
    weights = []
    for i,seq in enumerate(sequences):
        for j in range(0, len(seq)- k + 1):
            kmers.append(seq[j:j + motif_len])
            weights.append(E_zij[i][j])
    cm = makeCountMatrix(kmers, weights)
    cm = addPseudo(cm, pseudocount)
    fm = makeFrequencyMatrix(cm)
    wmm = makeWMM(fm, background)
    return wmm