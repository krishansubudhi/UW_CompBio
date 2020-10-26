from assignment2.main import align 
import os
import pandas as pd
import io
import numpy as np

table = '''
Species	Name	Description	Accession
Homo sapiens (Human)	MYOD1_HUMAN	Myoblast determination protein 1	P15172
Homo sapiens (Human)	TAL1_HUMAN	T-cell acute lymphocytic leukemia protein 1 (TAL-1)	P17542
Mus musculus (Mouse)	MYOD1_MOUSE	Myoblast determination protein 1	P10085
Gallus gallus (Chicken)	MYOD1_CHICK	Myoblast determination protein 1 homolog (MYOD1 homolog)	P16075
Xenopus laevis (African clawed frog)	MYODA_XENLA	Myoblast determination protein 1 homolog A (Myogenic factor 1)	P13904
Danio rerio (Zebrafish)	MYOD1_DANRE	Myoblast determination protein 1 homolog (Myogenic factor 1)	Q90477
Branchiostoma belcheri (Amphioxus)	Q8IU24_BRABE	MyoD-related	Q8IU24
Drosophila melanogaster (Fruit fly)	MYOD_DROME	Myogenic-determination protein (Protein nautilus) (dMyd)	P22816
Caenorhabditis elegans	LIN32_CAEEL	Protein lin-32 (Abnormal cell lineage protein 32)	Q10574
Homo sapiens (Human)	SYFM_HUMAN	Phenylalanyl-tRNA synthetase, mitochondrial	O95363
'''
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', -1)
pd.set_option('display.width', 2000)
df = pd.read_csv(io.StringIO(table),delimiter = '\t', index_col= 'Accession')
print(df.head(10))
proteins = df.index.values
total = len(proteins)

scores = pd.DataFrame(np.zeros( (total, total) ), index = proteins, columns = proteins)


for i in range(total):
    for j in range(i+1, total):
        score = align('proteins/'+proteins[i]+'.fasta', 'proteins/'+proteins[j]+'.fasta')
        scores.loc[proteins[i]][proteins[j]] = score
print(scores.head(10))
# align(args.seq1, args.seq2, args.permutations)

