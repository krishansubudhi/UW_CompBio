import random
import pandas as pd
import numpy as np

def get_seqs_from_files(file_paths : list):
    sequences = []
    for file_path in file_paths:
        sequences.extend(get_seqs_from_file(file_path))
    return sequences

def get_seqs_from_file(file_path:str):
    # assert filerpath.endswith('.fasta')
    sequences = []
    with open(file_path,'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith('>'):
            sequences.append('')
        else:
            line = line.strip().upper()
            line = ''.join([c if c in list('ACGT') else 'T' for c in line])
            sequences[-1] +=line
    return sequences

def print_random_seq(size = 50):
    seq = [list('ACGT')[random.randint(0,3)] for i in range(size)]
    print (''.join(seq))

def get_pseudo_count_vector():
    '''
        1   2
    A x+0 x+1
    C x+0 x+0
    T x+1 x+0
    G x+0 x+0

        1   2
    A .05 .85
    C .05 .05
    T .85 .05
    G .05 .05

    Assuming only a count of 1 for the seed seq
    x / (1+4x) = 0.05 = 1/20
    20x = 1 + 4x
    16x = 1
    x = 1/16
    '''
    return [1/16]*4

def get_seed_kmers(sequence, k):
    kmers = []
    for pos in np.arange(0,len(sequence),k//2):

        kmer = sequence[pos:pos+k]
        if len(kmer) == k:
            # print(pos+1)
            kmers.append(kmer)
    if len(sequence)%k > 0:
        # print(len(sequence)-k +1)
        kmer = sequence[len(sequence)-k:]
        assert len(kmer) == k
        kmers.append(kmer)

    return kmers



