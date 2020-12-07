#!/usr/bin/env python
# coding: utf-8

# # Assignment 5
# Krishan Subudhi : [ksubudhi@uw.edu](mailto:ksubudhi@uw.edu)
# 
# Student Number : 2040900
# 
# Date : 12/06/2020
# 
# ---

# For kernel errors:
#  
#     pip install --upgrade pywin32==225
# 
# https://stackoverflow.com/questions/58612306/how-to-fix-importerror-dll-load-failed-while-importing-win32api

# In[13]:


try:
    display()
    gff = '../data/GCF_000091665.1_ASM9166v1_genomic.gff'
    fna = '../data/GCF_000091665.1_ASM9166v1_genomic.fna'
except Exception as e:
    display = print
    gff = './data/GCF_000091665.1_ASM9166v1_genomic.gff'
    fna = './data/GCF_000091665.1_ASM9166v1_genomic.fna'

# import importlib
# importlib.reload(assignment5.markov)


# In[14]:


import sys
sys.path.append('..')
from assignment5.utils import get_seqs_from_file, get_reverse_complement, get_cds_from_file
from assignment5.orf import ORFFinder, ORFAnalyzer
from assignment5.markov import GeneModel
import pandas as pd
import numpy as np


# ## Fetch Sequence

# In[15]:

print('Fetching ORFs from fna file... takes few seconds')
genome = get_seqs_from_file(fna)[0]
finder = ORFFinder(genome)
orfs = [finder.get_all_orfs(rf ) for rf in (1,2,3)]
orfs = pd.concat(orfs,ignore_index=True)
#orfs = raw_orfs[raw_orfs.length>=5].copy()
orfs.head()


# ## Fetch Label

# In[16]:

print('Fetching CDSs from gff file.. takes few seconds')
cds = np.array(get_cds_from_file(gff))
true_orf_end = set(end-3 if  genome[end-3:end] in finder.stop_codons else end for end in cds[:,1])
len(true_orf_end)


# ## Create Markov model

# In[17]:


analyzer = ORFAnalyzer(orfs)
long_orfs = analyzer.get_long_ofs()
positive_seqs = finder.get_sequences(long_orfs)
bg_seqs = [get_reverse_complement(seq) for seq in positive_seqs]

model = GeneModel(k = 5, pseudo_count=1)
model.build(positive_seqs, bg_seqs)
# model.print_sample_counts()


# ## Merge Everything

# In[18]:



truth = [True if end in true_orf_end else False for end in orfs.end]
orfs['isCDS'] = truth

orf_sequences = finder.get_sequences(orfs)
scores = [model.get_loglikelihood_ratio(seq) if len(seq)>=5 else np.nan for seq in orf_sequences ]
orfs['scores'] = scores

orfs.head()


# # Results
# 
# Markov model parameters:
# k = 5, pseudo_count=1

# In[22]:



for rf in (1,2,3):
    rf_orf = orfs[orfs.frame == rf].reset_index()
    print('\nReading Frame : ', rf)
    print( 'Number of ORFs = ', len(rf_orf))
    print('Summary of the first and last : ')
    display(rf_orf.sort_values('start').iloc[[0,-1]])


# In[25]:


print('The total number of short ORFs = ', len(orfs[orfs.length<50]) )
print('The total number of long ORFs = ', len(orfs[orfs.length>1400]) )
print("The total number of simple plus strand CDSs found in GenBank = ", len(true_orf_end))


# P(T | AAGxy) and  Q(T | AAGxy) for the 16 possible combinations of x,y in A,C,G,T :

# In[29]:


model.print_sample_counts(display = display)


# In[30]:


print('\nsummary data for the first 5 short ORFs')
display(orfs[orfs.length<50].sort_values('start').head(5))

print('\nsummary data for the the first 5 long ORFs')
display(orfs[orfs.length>1400].sort_values('start').head(5))


# ### CDSs without stop codon at the end
# Extra: 
# Some CDSs found in gff files did nto have stop codons at the end

# In[13]:


print(f'\nExtra: ORFS which are CDS = {orfs.isCDS.sum()}, Total CDSs = {len(true_orf_end)}')
tend = true_orf_end.copy()
#stop_codons = {'TAA', 'TAG', 'TGA'}
for x in tend-set(orfs.end):
    print(x, genome[x-3:x], genome[x-3:x+3])


# In[31]:


import pickle
with open('orfs.pickle','wb') as f:
    pickle.dump(orfs, f)




