from .build_matrices import *
import matplotlib.pyplot as plt
import numpy as np

class Evaluator:
    def __init__(self, wmm, sequences, name = ''):
        self.name = name
        self.wmm = wmm
        self.sequences = sequences
        plt.style.use('ggplot')
        self.calculate_scores()
    
    def calculate_scores(self):
        self.scores = scanWMM(self.wmm, self.sequences)
    
    def plot_results(self):
        sequences = self.sequences[:2]
        scores = self.scores[:2]
        fig, axes = plt.subplots(len(scores),1, figsize = (14,len(sequences)*2), constrained_layout=True)
        # fig.set_tight_layout(True)
        fig.suptitle(f'WMM {self.name} Scores for each position in sequences')
        # fig.set_dpi(200)
        for ax, seq, score in zip(axes, sequences, scores):
            x = range(len(score))
            ax.bar(x, score)
            ax.set_xlabel('Sequence: '+ seq)
            ax.set_ylabel('scores')
            ax.set_xticks(x)
            ax.set_xticklabels(list(seq)[:len(x)])
        plt.show()
    
    def get_gold_positions(self, motif_pos, k):
        return motif_pos-k//2 , motif_pos+k-1-k//2

    def plot_highscore_histogram(self, gold_start= None, gold_end = None):
        sequences = self.sequences
        scores = self.scores

        fig, ax = plt.subplots(figsize = (14,2))
        fig.set_dpi(150)
        
        max_len = max([len(seq) for seq in sequences])
        c = np.zeros(max_len, dtype = int)
        for i,score in enumerate(scores):
            j = np.argmax(score)
            c[j] += 1
        
        x = np.arange(0,max_len)
        barlist = ax.bar(x,c)
        
        ax.set_title(f'WMM {self.name} High scores counts per position')
        ax.set_xticks(x)
        ax.set_xticklabels(x+1)
        ax.set_xlabel('position')
        ax.set_ylabel('count')
        ax.xaxis.set_major_locator(plt.MaxNLocator(30))

        if gold_start:
            for gold in range(gold_start-1, gold_end):
                barlist[gold].set_color('green')
        
        print(f'Most common location of the best motif hit in each sequence = {np.argmax(c)+1}')
        plt.show()
    
    def get_y(self, actual_motif_position):
        y_score = np.array(self.scores)
        y_true = np.zeros_like(y_score, dtype = int)
        y_true[:,actual_motif_position-1] = 1
        y_score = y_score.reshape(-1,1)
        y_true = y_true.reshape(-1,1)
        return y_score, y_true