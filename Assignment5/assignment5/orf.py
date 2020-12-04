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
            if end:
                #start, end, length
                orfs.append((start+1, end+1, end-start+1)) #starts from 1
                start = end + 1
            else:
                break
        return pd.DataFrame(orfs, columns = ['start','end','length'])

    def get_next_orf(self, sequence, start):
        end = None
        while  start <= len(sequence) - 3:
            codon = sequence[start:start+3]
            if codon in self.stop_codons:
                end = start+2 #return the last neucleotite
                break
            start +=3
        return end