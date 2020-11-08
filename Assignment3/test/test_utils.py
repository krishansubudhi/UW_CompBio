from assignment3.utils import *
def test_get_seqs_from_files():
    files = ['data/hw3-debug-train.fasta','data/hw3-debug-train.fasta']
    seqs = get_seqs_from_files(files)
    print(seqs)
    assert seqs[0] == 'ATTTTTATTCATCAAGTGTTTACTGTTTTATAACAAGCAAACTTGCAGTTTCAGCTGCTTGTTGCAACAGCTGTTGGTTTCTCTCTCAAGCAGCTGTGGGCTGGGGTGGG'
    assert len(seqs) == 10

def test_get_seed_kmers():
    kmers = get_seed_kmers('ATTTTTATTCATCAAGTGTTTACTGTTTTATAAC'[:20], 10)
    assert len(kmers) ==3
    assert kmers[0] == 'ATTTTTATTCATCAAGTGTTTACTGTTTTATAAC'[:10]

    kmers = get_seed_kmers('ATTTTTATTCATCAAGTGTTTACTGTTTTATAAC'[:21], 10)
    assert len(kmers) ==4