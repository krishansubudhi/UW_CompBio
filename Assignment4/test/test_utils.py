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