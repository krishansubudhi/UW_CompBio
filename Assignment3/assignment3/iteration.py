'''
1. Initialize
2. EM iteration
3. Evaluate
'''
from utils import *
from build_matrices import *
class EMProcess:
    def __init__(self, fasta_files, k = 10, background = [0.25]*4, pseudo_counts = [1,1,1,1]):
        self.fasta_files = fasta_files
        self.pseudo_counts = pseudo_counts
        self.background = background
        self.k = k
        self.sequences = utils.get_seqs_from_files(fasta_files)

    def initialize(self, seed_subseq, pseudo_counts):
        cm = makeCountMatrix([seed_subseq])
        cm = addPseudo(cm, pseudo_counts)
        fm = makeFrequencyMatrix(cm)
        self.wmm = makeWMM(fm, background)
    
    def iterate(self):
        expectations = Estep(self.wmm, self.sequences, self.background)
        self.wmm = Mstep(expectations, self.sequences, self.k, self.pseudo_counts, self.background)


