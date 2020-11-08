from build_matrices import *
import matplotlib.pyplot as plt
import numpy as np

class Evaluator:
    def __init__(self, wmm, sequences):
        self.wmm = wmm
        self.sequences = sequences
        plt.style.use('ggplot')
    
    def calculate_scores(self):
        self.scores = scanWMM(self.wmm, sequences)
    
    def plot_results():
        sequences = self.sequences
        scores = self.scores
        fig, axes = plt.subplots(len(scores),1, figsize = (14,len(sequences)*2), constrained_layout=True)
        # fig.set_tight_layout(True)
        fig.suptitle('WMM Scores for each position in sequences')
        fig.set_dpi(200)
        for ax, seq, score in zip(axes, sequences, scores):
            ax.bar(list(seq), score)
            ax.set_xlabel('Sequence: '+ seq)
            ax.set_ylabel('scores')
    
    def plot_highscore_histogram():
        sequences = self.sequences
        scores = self.scores
        fig, ax = plt.subplots(figsize = (6,2))
        fig.set_dpi(150)
        max_len = max([len(seq) for seq in sequences])
        c = np.zeros(max_len, dtype = int)
        for i,score in enumerate(scores):
            j = np.argmax(score)
            c[j] += 1
        ax.bar(range(1,max_len+1),c)
        ax.set_title('High scores counts per position')
        ax.set_xlabel('position')
        ax.set_ylabel('count')
        print(f'most common location of the best motif hit in each sequence = {np.argmax(c)+1}')