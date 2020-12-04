from collections import Counter
class MarkovModel():
    def __init__(self, k=5, pseudo_count = 1 ):
        self.k = k
        self.pseudo_count = pseudo_count
    
    def create_counts(self, sequences):
        def create_counts(seq):
            k = self.k
            if len(seq)<=k:
                return Counter()
            kgram_counter = Counter([seq[i:i+k] for i in range(len(seq)-k+1)])
            k1gram_counter = Counter([seq[i:i+k+1] for i in range(len(seq)-k)])
            return kgram_counter + k1gram_counter

        c = Counter()
        for seq in sequences:
            c += create_counts(seq)
        

        return c
    
