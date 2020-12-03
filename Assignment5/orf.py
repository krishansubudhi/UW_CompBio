class ORFFinder():
    def __init__(self):
        self.stop_codons = {'TAA', 'TAG', 'TGA'}
    
    def get_all_orfs(self, sequence , readingframe = 1):
        '''
        start and end positions, up to and including the last nucleotide of the stop codon following the ORF. 
        The numbering scheme counts the first position of the genome as 1, not zero.
        '''
        start = readingframe-1
        orfs = []
        while start<=len(sequence)-3:
            end = get_next_orf(sequence, start)
            #start, end, length
            orfs.append((start+1, end+1, end-start+1))
            start = end + 1
