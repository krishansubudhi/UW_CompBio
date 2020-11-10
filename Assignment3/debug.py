

import sys
sys.path.append('..')

import assignment3
# import importlib
# importlib.reload(assignment3.evaluator)

from assignment3.iteration import EMProcess
from assignment3.evaluator import Evaluator
from assignment3.utils import *
from assignment3.build_matrices import *
from assignment3.em import *
import matplotlib.pyplot as plt



train_files = ['data/hw3-debug-train.fasta']
test_files = ['data/hw3-debug-test.fasta']
train_sequences = get_seqs_from_files(train_files)
test_sequences = get_seqs_from_files(test_files)
k = 10
background = [0.25]*4
pseudo_counts = get_pseudo_count_vector()
print('Initialization pseudo_counts = ', pseudo_counts)


# # EM step

# In[3]:


def get_entropies(processes):
    entropies = np.array([p.wmm.entropy for p in processes])
    return entropies


# In[4]:


seeds = get_seed_kmers(train_sequences[0] ,k)

processes = []
all_entropies = {}
for seed in seeds:
    process = EMProcess(train_sequences, k , background)
    processes.append(process)
    process.initialize(seed,pseudo_counts)


# In[5]:



for i in range(3):
    print(f'EM Iteration {i+1}')
    for process in processes:
        process.iterate()
    all_entropies[i+1] = get_entropies(processes)


# ### ABC
# 
# For each of the S seed WMMs defined in "Initialization," do three E-step/M-step pairs. Among the resulting S WMMs, select three WMMs: the ones attaining the highest entropy (relative to background), the median entropy, and the lowest entropy. Call these WMMs A, B and C, respectively.
# 
# 

# In[6]:


entropies = np.array([p.wmm.entropy for p in processes])


highest, median, lowest = np.argmax(entropies), np.argsort(entropies)[len(entropies)//2], np.argmin(entropies)




# In[7]:


import copy
A, B, C = processes[highest].wmm, processes[median].wmm, processes[lowest].wmm
A,B,C = copy.deepcopy(A),copy.deepcopy(B),copy.deepcopy(C)


# ### Additional 7 rounds 
# Run an additional 7 E-step/M-step pairs on all S of the third-round WMMs (a total of 10 E-M rounds on each). 

# In[8]:


for i in range(7):
    print(f'EM Iteration {i+3+1}')
    for process in processes:
        process.iterate()
    all_entropies[i+1+3] = get_entropies(processes)


# ### D
# Select as your final "motif" the best (highest entropy) of the S candidates after round 10; call this WMM D.

# In[9]:


entropies_7 = np.array([p.wmm.entropy for p in processes])
print(entropies_7)
D = processes[np.argmax(entropies_7)].wmm


# ### Entropy table 
# As a simple descriptive summary of this process, print in a tidy-ish S row by 11 column table the entropies of each seed WMM and its 10 successive E-M-refined iterates.

# In[10]:


import pandas as pd
table = pd.DataFrame(all_entropies)
table['seed'] = seeds 
table = table[['seed'] + table.columns.tolist()[:-1]]
table.style.set_caption("Entropy : rows = seed numbers, columns = EM iterations")
print("Entropy : rows = seed numbers, columns = EM iterations")
print(table)


# ### Also print the frequency matrices for WMMs A, B, C, and D.

# In[11]:


fm = calculateProbabilities(A, background)
print(f'\n\nFrequency matrix for A')
print(fm)


# In[12]:


fm = calculateProbabilities(B, background)
print(f'\n\nFrequency matrix for B')
print(fm)


fm = calculateProbabilities(C, background)
print(f'\n\nFrequency matrix for C')
print(fm)



fm = calculateProbabilities(D, background)
print(f'\n\nFrequency matrix for D')
print(fm)




evals = []
for name, wmm in zip('ABCD', [A,B,C,D]):
    eval = Evaluator(wmm, test_sequences)
    eval.name = name
    evals.append(eval)
    # eval.plot_results()

    # combine scores and create y_true. Calculate ROC




motif_pos = 51
# print('gold_start, gold_end = ',gold_start, gold_end)
# print('Gold sequence = ',train_sequences[0][50:51+k])
for  eval in evals:
    eval.set_gold_positions()
    eval.plot_highscore_histogram()
plt.show(block=False)

# # ROC
# 
# Generate an ROC plot for your motif, and calculate AUC. 
# 
# To do this for a test set containing n sequences, you will have n * (113 - k + 1) WMM scores, n of them labeled True, and the rest False. 

# ### ROC plot

# In[22]:


from assignment3.roc import ROC
import matplotlib.pyplot as plt
rocs = []
# plt.set_color_cycle(['red', 'black', 'yellow'])
plt.figure()
for eval in evals:
    y_score, y_true = eval.get_y()
    r = ROC(y_true, y_score)
    rocs.append(r)
    r.plot_roc()
plt.legend([e.name for e in evals])
plt.show(block=False)


for eval, r in zip(evals, rocs):
    print(f'AUC for WMM {eval.name} = {r.calculateAUC():.3f}')


r = rocs[2]
t = r.largest_thres_TPR1()
print(f'WMM C: Largest Threshold with TPR 1 for = {t:.3f}')

tpr, fpr, tp, fp, tn, fn = r.get_TPR_FPR_TP_FP_TN_FN(t)
print('WMM C : At threshold f {:.3f} , TPR = {}, FPR = {:.3f}, tp = {}, fp = {}, tn = {}, fn = {}'.format(t, tpr, fpr, tp, fp, tn, fn))

plt.show()
