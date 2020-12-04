from assignment5.utils import get_seqs_from_file 
from assignment5.orf import ORFFinder

genome = get_seqs_from_file('data/GCF_000091665.1_ASM9166v1_genomic.fna')[0]
print('Length of genome is', len(genome))

orfs = ORFFinder().get_all_orfs(genome)
print(orfs.head())