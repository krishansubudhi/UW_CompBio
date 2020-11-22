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