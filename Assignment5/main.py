#!/usr/bin/env python
# coding: utf-8

# For kernel errors:
#  
#     pip install --upgrade pywin32==224
# 
# https://stackoverflow.com/questions/58612306/how-to-fix-importerror-dll-load-failed-while-importing-win32api

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
# import importlib
# importlib.reload(assignment5.markov)


# In[2]:


import sys
sys.path.append('..')
from assignment5.utils import get_seqs_from_file, get_reverse_complement, get_cds_from_file
from assignment5.orf import ORFFinder, ORFAnalyzer
from assignment5.markov import GeneModel
import pandas as pd
import numpy as np


# ## Fetch Sequence

# In[3]:


genome = get_seqs_from_file('../data/GCF_000091665.1_ASM9166v1_genomic.fna')[0]
finder = ORFFinder(genome)
orfs = [finder.get_all_orfs(rf ) for rf in (1,2,3)]
orfs = pd.concat(orfs,ignore_index=True)
#orfs = raw_orfs[raw_orfs.length>=5].copy()
orfs.head()


# ## Fetch Label

# In[16]:


cds = np.array(get_cds_from_file('../data/GCF_000091665.1_ASM9166v1_genomic.gff'))
true_orf_end = set(end-3 if  genome[end-3:end] in finder.stop_codons else end for end in cds[:,1])
len(true_orf_end)


# ## Create Markov model

# In[71]:


analyzer = ORFAnalyzer(orfs)
long_orfs = analyzer.get_long_ofs()
positive_seqs = finder.get_sequences(long_orfs)
bg_seqs = [get_reverse_complement(seq) for seq in positive_seqs]

model = GeneModel(k = 5, pseudo_count=1)
model.build(positive_seqs, bg_seqs)


# In[72]:


model.print_sample_counts()


# ## Merge Everything

# In[73]:



truth = [True if end in true_orf_end else False for end in orfs.end]
orfs['isCDS'] = truth

orf_sequences = finder.get_sequences(orfs)
scores = [model.get_loglikelihood_ratio(seq) if len(seq)>=5 else np.nan for seq in orf_sequences ]
orfs['scores'] = scores

orfs.head()


# # Results

# In[74]:


for rf in (1,2,3):
    rf_orf = orfs[orfs.frame == rf]
    print('\nReading Frame : ', rf)
    print( 'Number of ORFs = ', len(rf_orf))
    print('Summary of the first and last : ')
    display(rf_orf.sort_values('start').iloc[[0,-1]])


# In[75]:


print('The total number of short ORFs = ', len(orfs[orfs.length<50]) )
print('The total number of long ORFs = ', len(orfs[orfs.length>1400]) )


# In[76]:


print("The total number of simple plus strand CDSs found in GenBank = ", len(true_orf_end))


# In[77]:


print('P(T | AAGxy), Q(T | AAGxy) for the 16 possible combinations of x,y in A,C,G,T :')
model.print_sample_counts()


# In[78]:


print('summary data for the first 5 short ORFs')
display(orfs[orfs.length<50].sort_values('start').head(5))

print('summary data for the the first 5 long ORFs')
display(orfs[orfs.length>1400].sort_values('start').head(5))


# ### CDSs without stop codon at the end

# In[79]:


print(f'ORFS which are CDS = {orfs.isCDS.sum()}, Total CDSs = {len(true_orf_end)}')
tend = true_orf_end.copy()
#stop_codons = {'TAA', 'TAG', 'TGA'}
for x in tend-set(orfs.end):
    print(x, genome[x-3:x], genome[x-3:x+3])

