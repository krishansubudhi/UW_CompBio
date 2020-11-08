from .build_matrices import *
import matplotlib.pyplot as plt
import numpy as np

class Evaluator:
    def __init__(self, wmm, sequences):
        self.wmm = wmm
        self.sequences = sequences
        plt.style.use('ggplot')
        self.calculate_scores()
    
    def calculate_scores(self):
        self.scores = scanWMM(self.wmm, self.sequences)
    
    def plot_results(self, ):
        sequences = self.sequences
        scores = self.scores
        fig, axes = plt.subplots(len(scores),1, figsize = (14,len(sequences)*2), constrained_layout=True)
        # fig.set_tight_layout(True)
        fig.suptitle('WMM Scores for each position in sequences')
        # fig.set_dpi(200)
        for ax, seq, score in zip(axes, sequences, scores):
            ax.bar(range(len(score)), score)
            ax.set_xlabel('Sequence: '+ seq)
            ax.set_ylabel('scores')
            ax.set_xticklabels(list('0'+seq))
        plt.show()
    
    def get_gold_positions(self, motif_pos, k):
        return motif_pos-k//2 , motif_pos+k-1-k//2

    def plot_highscore_histogram(self, gold_start, gold_end):
        sequences = self.sequences
        scores = self.scores

        fig, ax = plt.subplots(figsize = (4,2))
        fig.set_dpi(150)
        max_len = max([len(seq) for seq in sequences])
        c = np.zeros(max_len, dtype = int)
        for i,score in enumerate(scores):
            j = np.argmax(score)
            c[j] += 1
        barlist = ax.bar(range(0,max_len),c)
        ax.set_title('High scores counts per position')
        ax.set_xticklabels(range(0,max_len+1))
        ax.set_xlabel('position')
        ax.set_ylabel('count')

        for gold in range(gold_start-1, gold_end):
            barlist[gold].set_color('green')
        print(f'Most common location of the best motif hit in each sequence = {np.argmax(c)+1}')
        plt.show()