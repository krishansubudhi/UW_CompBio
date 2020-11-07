# Instructions

This file will provide instructions to run assignment3 code.
https://courses.cs.washington.edu/courses/csep527/20au/hw/hw3.html

**The Goal:** The goal of this assignment is to investigate a MEME-like algorithm for sequence motif discovery. In brief, you will be given a list of (unaligned) sequences of varying lengths, **most or all of which contain one instance of a "motif"** (i.e., a short, approximately repeated subsequence), and the goal is to discover it, to build a weight matrix model (WMM, aka PWM or PSSM) capturing the pattern, and to use it to search for other instances of the motif in additional sequences. For scale, think of your **input as consisting of at most a few hundred sequences, each at most a few hundred nucleotides in length, and the motif is 10-20 nucleotides long.**

## count matrix
Given a 
list *M*

**containing *n* sequences**, 
**each of length *k*** 

that are **all presumed to be instances of one motif**

the ***count matrix*** representing it is a **4 by *k* table** 
whose *i, j* entry (*1 ≤ i ≤ 4, 1 ≤ j ≤ k*) is the** **count of the number of times nucleotide *i* appears in position *j***** in a string in *M*.**

rows 1, 2, 3, 4 should correspond to nucleotides A, C, G, T in that order

each column of such count table should sum to the same number

before pseudocounting, this number will be *n*, the number of sequences in *M*; after pseudocounting, it will be *n+p*, where *p* is the sum of the pseudocount vector.

## A *frequency matrix*
is another 4 by *k* table, giving the **fraction of each nucleotide at each position**, i.e., the result of dividing each entry in a count matrix by the sum of the corresponding column. (Depending on context, **"counts" might be before or after adding pseudocounts**. Column sums in the frequency matrix should be 1.0 in either case.)

## *weight matrix*
The corresponding *weight matrix* (WMM) is another 4 by *k* table whose *i,j* entry is the base 2 logarithm of the ratio of the frequency matrix entry to the background frequency of that nucleotide. (For simplicity in my slides, I scaled these log ratios by a factor of 10 and rounded them to integers. Do *not* do this in your program.)

## Inputs
Your key inputs will be FASTA **files**, each containing several sequences. 
  1. File format is as in assignment 1, except that it's DNA, not protein. 
  2. Both upper- and lower-case ACGT should be allowed, and treated equivalently.
  3. (Other non-whitespace should be replaced by T. This is not what I'd do in production code, but simple.) 

I will provide four specific .fasta files ( [hw3-debug-train.fasta](https://courses.cs.washington.edu/courses/csep527/20au/hw/hw3-debug-train.fasta), [hw3-debug-test.fasta](https://courses.cs.washington.edu/courses/csep527/20au/hw/hw3-debug-test.fasta), [hw3-train.fasta](https://courses.cs.washington.edu/courses/csep527/20au/hw/hw3-train.fasta), [hw3-test.fasta](https://courses.cs.washington.edu/courses/csep527/20au/hw/hw3-test.fasta) ) for your use. 
>mm9_chrX:153872924-153872936(-)
ATTTTTATTCATCAAGTGTTTACTGTTTTATAACAAGCAAACTTGCAGTTTCAGCTGCTTGTTGCAACAGCTGTTGGTTT
CTCTCTCAAGCAGCTGTGGGCTGGGGTGGG
>mm9_chr11:119492995-119493007(+)
ACAGCTAGTGCTGTGTGTGCATTGGTGTGTCTGCAGGCGGCAGGGCACCTGTTCTTAGTGACTGGGCCTGGCCTGGATTA
GCTTGGTCCTTGGCTAAAGGTTTTGT
>mm9_chr15:31242332-31242344(+)
TGTGCTCTCCGGCTACTGACACTCGTCCAGCTGTGACTGAACGGCCTCCCAACAGCTGTCCATCAATACTGTGGTGAACC
AGATGCTTGTCCATTCTGTTCCT
>mm9_chr15:75921796-75921808(+)
TCTATCCTTAGGCTACGGGACGGCGGCGTCACCCGCACCCGTGCCCACCTGCTCCCGCCGCTTCTGCCAGCGGCCACACG
GGCTCTCCTCCAGGATGTCGCTCTCG
>mm9_chr1:80073137-80073149(+)
CGCACTGACTGCCCTTGCAGATCACACTGGCTTTGGCTCCCAACCTCCCAACCACCTGTTACTCCAGTTCCAAGTGATCT
AATGCTCTCCTCTGACCTCTGT

I *strongly* suggest that you do your initial debugging and testing on files that you make up yourself. 
1. "Plant" a motif of your own choosing amidst **random flanking sequence** of 50-100 bases in a total of 2-10 sequences. 
2. Start with short ones with near-identical motifs, and gradually make it more difficult. 
3. Train (see below) on that and test (see below) on the same or an additional set of synthetic sequences. 
4. Once you are satisfied with your performance on that, try it on my "debug" data sets, which will have about 10 sequences. 
5. To promote "crowd-sourced debugging," you may post results on my "debug" sets on the course discussion board. (Just for fun, include your choice of programming language, approximate code length, and runtime on this small example.) 
6. Finally, run your motif discovery algorithm on my "training" data set, and test the result on my "test" data set, as described below.


## Assumption (Important)
1. Assume a motif width of *k=10*, and 
2. use (0.25, 0.25, 0.25, 0.25) as your background 
3. and **pseudocount vectors **
4. **(except as noted under "Initialization").**