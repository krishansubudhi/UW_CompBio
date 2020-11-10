
import sys
sys.path.append('..')

import assignment3
# import importlib
# importlib.reload(assignment3.evaluator)

from assignment3.iteration import EMProcess
from assignment3.evaluator import Evaluator
from assignment3.utils import *
from assignment3.build_matrices import *
from assignment3.em import *
import matplotlib.pyplot as plt

train_files = ['data/hw3-debug-train.fasta']
test_files = ['data/hw3-debug-test.fasta']
train_sequences = get_seqs_from_files(train_files)
test_sequences = get_seqs_from_files(test_files)
k = 10
background = [0.25]*4
pseudo_counts = get_pseudo_count_vector()
print('pseudo_counts = ', pseudo_counts)

def get_entropies(processes):
    entropies = np.array([p.wmm.entropy for p in processes])
    return entropies

seeds = get_seed_kmers(train_sequences[0] ,k)

processes = []
all_entropies = {}
for seed in seeds:
    process = EMProcess(train_sequences, k , background)
    processes.append(process)
    process.initialize(seed,pseudo_counts)
entropies = np.array([p.wmm.entropy for p in processes])


for i in range(3):
    for process in processes:
        process.iterate()
    all_entropies[i+1] = get_entropies(processes)
