from collections import Counter
class MarkovModel():
    def __init__(self, k=5, pseudo_count = 1 ):
        self.k = k
        self.pseudo_count = pseudo_count
    
    def build(self, positive_seqs, background_seqs):
        self.p_counts, self.p1_counts = self.create_counts(positive_seqs)


        self.q_counts, self.q1_counts = self.create_counts(background_seqs)


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
    
