from assignment3.iteration import EMProcess
from assignment3.evaluator import Evaluator
from assignment3.utils import *

files = ['data/my.fasta']

sequences = get_seqs_from_files(files)

k = 5

process = EMProcess(sequences, k , background = [0.25]*4)

pseudo_counts = get_pseudo_count_vector()


seeds = get_seed_kmers(sequences[0] ,k)

process.initialize(seeds[0],pseudo_counts)

for i in range(3):
    process.iterate()

test_seq = sequences
eval = Evaluator(process.wmm, test_seq)


eval.plot_results()

# combine scores and create y_true. Calculate ROC
