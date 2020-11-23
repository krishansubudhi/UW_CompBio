
'''
Krishan Subudhi (ksubudhi@uw.edu) 
Student number: 2040900
'''

import sys
from assignment4.train import *
from assignment4.utils import get_seqs_from_file,get_genes_from_file
import time

display = print

emmisionP = pd.DataFrame([ [0.25]*4, 
                            [0.2,0.3,0.3,0.2] ], 
                            index = ['State 1','State 2'], columns = list('ACGT'))
transitionP = pd.DataFrame([[0.9999, 0.0001],
                            [0.9999,0.0001], 
                            [0.01, 0.99]], 
                            columns = ['State 1','State 2'], index = ['Begin','State 1','State 2'])


sequence_all = get_seqs_from_file('data/GCF_000091665.1_ASM9166v1_genomic.fna')[0]

k = 10

pseudo_count = 0.1


print(f'Length of the DNA is {len(sequence_all)}')
print(sequence_all[:50], '.....', sequence_all[-50:])

sequence = sequence_all

# Train

total_iter = 10
start = time.time()
path = None

trainer = ViterbiTrain(sequence, emmisionP, transitionP, 'Begin', pseudo_count, debug = False)

for i in range(total_iter + 1):
    print(f'\n\n************** Iteration {i} ************')
    print('_______________________________________\n')
    
    start_viterbi = time.time()
    path, v_all = trainer.expectation()
    end_viterbi = time.time()
    print(f'\n***Viterbi time iteration {i} = {end_viterbi-start_viterbi} seconds')
    trainer.viterbi.print(v_all, hit_state = 'State 2', path = path.copy(), k = 10 if i <10 else 0)
    if i < total_iter:
        trainer.maximization(path)

end = time.time()
print(f'Total time taken = {end-start} seconds')

# Evaluate

hits = trainer.viterbi.get_hits(path)
hits = hits[hits.state == 'State 2'].reset_index(drop=True)



print('Table 1: First 10 hits longer than 50 bp from the 10th pass:' )
hits_gt50bp = hits[hits.length > 50*2]
df = hits_gt50bp.head(10).reset_index(drop = True) 
display(df)



genepos = get_genes_from_file('data/GCF_000091665.1_ASM9166v1_genomic.gff')
genepos = pd.DataFrame(genepos, columns = ['start', 'end'])
genepos['length'] = genepos['end'] - genepos['start']
print('Table 2 :top 30 gold gene positions:')
display(genepos.head(30))



def overlap_count(t1, t2):
    overlap = set(range(t1[0], t1[1]+1)) & set(range(t2[0], t2[1]+1))
    return len(overlap)


iter_pred = iter(hits_gt50bp[['start', 'end']].head(10).values)
iter_gold = iter(genepos[['start', 'end']].values)
overlap_ratios = []
overlaps =[]
gold = next(iter_gold)
for pred in iter_pred:
    gene_overlaps = []
    length = pred[1]-pred[0]
    overlap = 0
    while pred[1] > gold[0]:
        c = overlap_count(pred, gold)
        overlap += c
        if c> 0:
            gene_overlaps.append(gold)
        gold = next(iter_gold)
    overlap_ratios.append(overlap/length)
    overlaps.append(gene_overlaps)

# Matches with 50% overlap threshold with gold positions :

df['percentage_overlap'] = np.array(overlap_ratios)*100
df['overlaps'] =overlaps
df['match'] = df['percentage_overlap'] >50
print("Table 3: Percentage overlap - predicted gene (> 50bp) vs gold genes")
display(df)


## Plot

import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1)
fig.set_figwidth(17)
fig.set_figheight(1)
for s,e in df[['start','end']].values:
    ax.plot([s,e],[2,2], linewidth=10,  color = 'blue', marker='|', markeredgecolor='red', markersize=10)

for s,e in genepos[['start', 'end']].values:
    if s < 650000:
        ax.plot([s,e],[1,1], linewidth=10, marker='|', color = 'green', markeredgecolor='red', markersize=10)

ax.set_title('Gene position prediction : top (predicted), bottom(Gold)')
ax.set_xlabel('position')
ax.margins(0.1) 
plt.show()
