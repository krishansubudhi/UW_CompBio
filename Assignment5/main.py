from assignment5.utils import get_seqs_from_file, get_reverse_complement, get_cds_from_file
from assignment5.orf import ORFFinder, ORFAnalyzer
from assignment5.markov import GeneModel
import pandas as pd
import numpy as np

genome = get_seqs_from_file('data/GCF_000091665.1_ASM9166v1_genomic.fna')[0]
print('Length of genome is', len(genome))

orfs = []
for rf in (1,2,3):
    orf = ORFFinder().get_all_orfs(genome, rf )
    print(rf, len(orf))
    print(orf.head())
    orfs.append(orf)
orfs = pd.concat(orfs,ignore_index=True)
print('Total ORFs = ',len(orfs))

analyzer = ORFAnalyzer(orfs)
long_orfs = analyzer.get_long_ofs()

print('Long ORFs', len(long_orfs))
print(long_orfs.sort_values('start').head())
positive_seqs = [ genome[record['start']-1:record['end']] for record in long_orfs.to_dict('records')]
print(len(positive_seqs))
bg_seqs = [get_reverse_complement(seq) for seq in positive_seqs]

markov = GeneModel(k = 5, pseudo_count=1)
markov.build(positive_seqs, bg_seqs)

print('Foreground T|AAGxy counts')
print(pd.DataFrame(
        [[markov.foreground.p1_counts['AAG'+x+y+'T'] for y in 'ACGT'] for x in 'ACGT'],
        columns = list('ACGT'),
        index = list('ACGT')
    )
)

print('Background T|AAGxy counts')
print(pd.DataFrame(
        [[markov.background.p1_counts['AAG'+x+y+'T'] for y in 'ACGT'] for x in 'ACGT'],
        columns = list('ACGT'),
        index = list('ACGT')
    )
)

cds = np.array(get_cds_from_file('data/GCF_000091665.1_ASM9166v1_genomic.gff'))
true_orf_end = set(cds[:,1]-3)
# print(true_orf_end)
assert 4563 in true_orf_end

truth = [True if end in true_orf_end else False for end in orfs.end]
orfs['isCDS'] = truth
print('Total true ORFS = ', orfs.isCDS.sum())
print(orfs.head())
