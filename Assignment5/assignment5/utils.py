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


def get_cds_from_file(file_path:str):
    '''
    head -n 3700 *gff | grep "Protein Homology	CDS	[0-9]*	[0-9]*	.	+" > plusgenes-subset.gff
    '''
    genepos = []
    with open(file_path,'r') as file:
        lines = file.readlines()
    # print(lines)
    pattern = "Protein Homology	CDS	[0-9].*	[0-9].*	.	\\+"
    for i,line in  enumerate(lines):
        
        if i<3700 and re.search(pattern, line):
            # print(line)
            line = line.split()
            # print(line)
            genepos.append((int(line[4]),int(line[5])))
    return genepos

def get_reverse_complement(sequence):
    comps = {
        'A':'T',
        'C':'G',
        'T':'A',
        'G':'C'
    }
    complement =  ''.join([comps[nt] for nt in sequence])
    return complement[::-1]
