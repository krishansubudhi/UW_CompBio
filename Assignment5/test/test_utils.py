from assignment5.utils import *
def test_get_cds_from_file():
    cds = get_cds_from_file('data/GCF_000091665.1_ASM9166v1_genomic.gff')
    assert (4252,4566) in cds	
    assert (28018,28572) not in cds , 'exclude - strand'
    assert (6383,6817) not in cds, 'other chromosome'
    assert (97426,97537) not in cds, 'it\'s a trna'
    # subtract 3 from the end position 