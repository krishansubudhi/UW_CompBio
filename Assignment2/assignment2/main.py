'''
@author: Krishan Subudhi (Student No: 2040900) (ksubudhi@uw.edu)
'''

import sys, re
from assignment2.local_alignment import LocalAlignment
from assignment2.aligned_pair import AlignedPair
from assignment2.score import get_score_matrix

def get_seq_from_file(file_path:str):
    # assert filerpath.endswith('.fasta')
    with open(file_path,'r') as file:
        return ''.join([line for line in file if not line.startswith('>')])

def preprocess( seq1):
    seq1 = get_seq_from_file(seq1) if seq1.endswith('.fasta') else seq1
    seq1 = seq1.upper()

    amino_acids = {'A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V'}
    seq1 = [a for a in seq1 if a in amino_acids]

    return seq1

import copy
import random
def get_random_permutation(seq):
    seq = copy.deepcopy(seq)
    for i in range (len(seq)-1,0,-1):
        j = random.randint(0,i)
        seq[i] , seq[j] = seq[j], seq[i]
    return seq

def align(seq1, seq2, random_permutations = 0) :
    print('\n-----\n')
    accession1 = re.split(r'[\\/.]+',seq1)[-2] if seq1.endswith('.fasta') else 'seq1'
    accession2 = re.split(r'[\\/.]+',seq2)[-2] if seq2.endswith('.fasta') else 'seq2'


    scoring_matrix = get_score_matrix('blosum62.txt')
    
    print('{} vs {}'.format(seq1,seq2))

    seq1, seq2 = preprocess(seq1), preprocess(seq2)
    aligner = LocalAlignment(scoring_matrix, gap_penalty = -4)

    pair, best_score, best_score_matrix = aligner.get_best_alignment( seq1, seq2)
    
    if len(seq1)<15 and len(seq2)<15:
        print(best_score_matrix)
    
    pair.print_alignment(accession1, accession2, scoring_matrix)

    print('\nScore = {}'.format(best_score))

    k = 0
    n = 0
    if random_permutations >0 :
        for i in range(random_permutations):
            permuted = get_random_permutation(seq2)
            _, score, _ = aligner.get_best_alignment( seq1, permuted)
            if score >= best_score:
                k +=1
            n += 1
            #print(k,n, score, permuted)
    
        print('Emperical P-value ({} permutations )= {:.3E}'.format(
            random_permutations,
            (k+1) / (n+1)
        ))
    
    print('\n-----\n')
    return best_score

