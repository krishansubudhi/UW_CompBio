from collections import Counter
import numpy as np
import pandas as pd
import math
class MarkovModel():
    def __init__(self, k=5, pseudo_count = 1 ):
        self.k = k
        self.pseudo_count = pseudo_count
    
    def build(self, seqs):
        self.p_counts, self.p1_counts = self.create_counts(seqs)
        self.p_total = sum(self.p_counts.values())
    
    # SIMPLIPY THIS
    def get_count(self,kmer):
        if len(kmer) == self.k+1:
            return self.p1_counts[kmer] +self.pseudo_count
        else:
            return self.p_counts[kmer[:-1]] +self.pseudo_count * 4
    
    def get_probability(self, kmer):
        k = self.k
        if len(kmer) == self.k+1:
            return ((self.p1_counts[kmer] +self.pseudo_count)/ 
            (self.p_counts[kmer[:-1]] +self.pseudo_count * 4)) # conditional probability with pseudo count
        else:
            # not using pseudo count here. can be problematic 
            # It's not clear what value to add in denominator.
            # If x is added to the denominator, (4^k)*x should be added to the denominator since there can be  4^k possible kmers
            return (self.p_counts[kmer]+ self.pseudo_count) / (self.p_total + math.pow(4,k) * self.pseudo_count)

    def get_log_p(self, kmer):
        # print(kmer)
        p = self.get_probability(kmer)
        assert p>0, f'add pseudo count {kmer}'
        return np.log(p)
    
    def get_loglikelihood(self,seq):
        k = self.k
        ll = self.get_log_p(seq[:k])
        for i in range(len(seq)-k):
            ll += self.get_log_p(seq[i:i+k+1])
        
        return ll

    def create_counts(self, sequences):
        def create_counts(seq):
            k = self.k
            if len(seq)<=k:
                return Counter(), Counter()
            kgram_counter = Counter([seq[i:i+k] for i in range(len(seq)-k+1)])
            k1gram_counter = Counter([seq[i:i+k+1] for i in range(len(seq)-k)])
            return kgram_counter , k1gram_counter

        c, c1 = Counter(), Counter()
        for seq in sequences:
            k, k1= create_counts(seq)
            c += k
            c1 += k1
        return c, c1
    
class GeneModel():
    def __init__(self,  k=5, pseudo_count = 1):
        self.foreground = MarkovModel(k, pseudo_count)
        self.background = MarkovModel(k, pseudo_count)
    
    def build(self, fgseqs, bgseqs):
        self.foreground.build(fgseqs)
        self.background.build(bgseqs)
    
    def get_loglikelihood_ratio(self,seq):
        return self.foreground.get_loglikelihood(seq) - self.background.get_loglikelihood(seq)

    def print_sample_counts(self, display = print):
        print('\nForeground T|AAGxy counts for P(T | AAGxy) = ')
        display(pd.DataFrame(
                [[self.foreground.p1_counts['AAG'+x+y+'T'] for y in 'ACGT'] for x in 'ACGT'],
                columns = list('ACGT'),
                index = list('ACGT')
            )
        )

        print('\nBackground T|AAGxy counts for Q(T | AAGxy) = ')
        display(pd.DataFrame(
                [[self.background.p1_counts['AAG'+x+y+'T'] for y in 'ACGT'] for x in 'ACGT'],
                columns = list('ACGT'),
                index = list('ACGT')
            )
        )
