import unittest
import tempfile
from assignment4.utils import *
import os
def test_get_seqs_from_file():
    filepath = os.path.join(tempfile.gettempdir(), 'seqs.fasta')
    print(filepath)
    with open(filepath, 'w') as f:
        f.writelines(['>some header\n', 
                        'ACgTx \n',
                        'BatGgC\n', 
                      '>another header\n', 
                        'ACTG\n'])
    sequences = get_seqs_from_file(filepath)
    print(sequences)
    assert len(sequences) == 2
    assert sequences[0] == 'ACGTTTATGGC'
    assert sequences[1] == 'ACTG'

def test_get_genes_from_file():
    content ='''
    NC_000909.1  RefSeq       gene  97426  97537  .  -  .   ID=gene102;Dbxref=GeneID:1450942;Name=MJ_RS00515;gbkey=Gene;gene_biotype=tRNA;locus_tag=MJ_RS00515;old_locus_tag=MJ_t01%2CMJt01%2CtRNA-Met-1
    NC_000909.1  tRNAscan-SE  tRNA  97426  97537  .  -  .   ID=rna0;Parent=gene102;Dbxref=GeneID:1450942;anticodon=(pos:complement(97501..97503));gbkey=tRNA;inference=COORDINATES: profile:tRNAscan-SE:1.23;product=tRNA-Met
    NC_000909.1  tRNAscan-SE  exon  97500  97537  .  -  .   ID=id2;Parent=rna0;Dbxref=GeneID:1450942;anticodon=(pos:complement(97501..97503));gbkey=tRNA;inference=COORDINATES: profile:tRNAscan-SE:1.23;product=tRNA-Met
    NC_000909.1  tRNAscan-SE  exon  97426  97464  .  -  .   ID=id3;Parent=rna0;Dbxref=GeneID:1450942;anticodon=(pos:complement(97501..97503));gbkey=tRNA;inference=COORDINATES: profile:tRNAscan-SE:1.23;product=tRNA-Met
    '''
    filepath = os.path.join(tempfile.gettempdir(), 'genes.gff')
    with open(filepath, 'w') as f:
        f.write(content)
    genepos = get_genes_from_file(filepath)
    print(genepos)
    assert genepos[0] == (97426, 97537)
