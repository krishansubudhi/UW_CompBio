import pandas as pd

def get_seqs_from_file(file_path:str):
    # assert filerpath.endswith('.fasta')
    sequences = []
    with open(file_path,'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith('>'):
            sequences.append('')
        else:
            line = line.strip().upper()
            line = ''.join([c if c in list('ACGT') else 'T' for c in line])
            sequences[-1] +=line
    return sequences

import re
def get_genes_from_file(file_path:str):
    # assert filerpath.endswith('.fasta')
    genepos = []
    with open(file_path,'r') as file:
        lines = file.readlines()
    for line in lines:
        if re.search('biotype=.*RNA',line):
            line = line.split()
            genepos.append((int(line[3]),int(line[4])))
    return genepos



def find_overlap(hits:pd.DataFrame, genepos:pd.DataFrame):
    def overlap_count(t1, t2):
        overlap = set(range(t1[0], t1[1]+1)) & set(range(t2[0], t2[1]+1))
        return len(overlap)
    
    iter_pred = iter(hits[['start', 'end']].values)
    iter_gold = iter(genepos[['start', 'end']].values)
    overlap_lengths = []
    overlap_genes =[]
    gold = next(iter_gold)
    for pred in iter_pred:
        gene_overlaps = []
        overlap = 0
        while pred[1] > gold[0]:
            c = overlap_count(pred, gold)
            overlap += c
            if c> 0:
                gene_overlaps.append(gold)
            try:
                gold = next(iter_gold)
            except StopIteration:
                break
        overlap_lengths.append(overlap)
        overlap_genes.append(gene_overlaps)
    return overlap_lengths, overlap_genes
