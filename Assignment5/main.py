from assignment5.utils import get_seqs_from_file, get_reverse_complement
from assignment5.orf import ORFFinder, ORFAnalyzer
from assignment5.markov import MarkovModel
import pandas as pd

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

markov = MarkovModel(k = 5, pseudo_count=1)
markov.build(positive_seqs, bg_seqs)

print(pd.DataFrame(
        [[markov.p1_counts['AAG'+x+y+'T'] for y in 'ACGT'] for x in 'ACGT'],
        columns = list('ACGT'),
        index = list('ACGT')
    )
)

print(pd.DataFrame(
        [[markov.q1_counts['AAG'+x+y+'T'] for y in 'ACGT'] for x in 'ACGT'],
        columns = list('ACGT'),
        index = list('ACGT')
    )
)
