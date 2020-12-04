import pandas as pd
class ORFFinder():
    def __init__(self):
        self.stop_codons = {'TAA', 'TAG', 'TGA'}
    
    def get_all_orfs(self, sequence , readingframe = 1):
        '''
        start and end positions, up to and including the last nucleotide of the stop codon following the ORF. 
        The numbering scheme counts the first position of the genome as 1, not zero.
        '''
        assert 1<=readingframe<=3
        start = readingframe-1
        orfs = []
        while start<=len(sequence)-3:
            end = self.get_next_orf(sequence, start)
            if end>start:
                #start, end, length
                orfs.append((start+1, end+1, end-start+1, readingframe)) #starts from 1
            start = end + 4
        return pd.DataFrame(orfs, columns = ['start','end','length','frame'])

    def get_next_orf(self, sequence, start):
        end = start-1
        while  start <= len(sequence) - 3:
            codon = sequence[start:start+3]
            if codon in self.stop_codons:
                break
            end = start+2 #move end to the current codon since it's not a stop codon
            start +=3 # move start to the next codon
        return end

class ORFAnalyzer():
    def __init__(self, orfs:pd.DataFrame):
        self.orfs = orfs
        self.long_t = 1400
        self.short_t = 5
    
    def get_long_ofs(self):
        return self.orfs[self.orfs.length>self.long_t]
    
    def get_short_ofs(self):
        return self.orfs[self.orfs.length<self.short_t]
    
