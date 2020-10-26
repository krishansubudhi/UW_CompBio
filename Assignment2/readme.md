# Get started

Assignment homepage: https://courses.cs.washington.edu/courses/csep527/20au/hw/hw2.html



## Create conda environemnt and install dependencies

Install miniconda from https://docs.conda.io/en/latest/miniconda.html

Run these commands in terminal

    conda create -n compbio python==3.8
    conda activate compbio
    pip install -r 

## Blosum62

[Downloaded Table](blosym62.txt)

## Proteins

1. MYOD1_HUMAN (P15172)

    Myoblast determination protein 1

    Acts as a transcriptional activator that promotes transcription of muscle-specific target genes and 
    
    plays a major role in regulating muscle differentiation.

2. TAL1_HUMAN (P17542)

    T-cell acute lymphocytic leukemia protein 1

    hemopoietic : Pertaining to or related to the formation of blood cells.

    malignancies: The property or condition of being malignant

    Implicated in the genesis of hemopoietic malignancies. It may play an important role in hemopoietic differentiation.

    - creates blood cell deferenciation
    blood cells differentiate from stem cells constatly. Stem cells are kind of base class for all blood cells

3. MYOD1_MOUSE (P10085)

    Myoblast determination protein 1

    Acts as a transcriptional activator that promotes transcription of muscle-specific target genes and plays a role in muscle differentiation

    -- Looks very similar to Myod1_human (no 1)

4. MYOD1_CHICK (P16075)
    
    Myoblast determination protein 1 homolog

    Acts as a transcriptional activator that promotes transcription of muscle-specific target genes and plays a role in muscle differentiation. 

    similar to 1

5. MYODA_XENLA (P13904)

    Organism
    Xenopus laevis (African clawed frog)

    Myoblast determination protein 1 homolog A

    **May** act as a transcriptional activator that promotes transcription of muscle-specific target genes and plays a role in muscle differentiation.

    Might be similar to other myod1 protein but looks slightly different. 

6. MYOD1_DANRE (Q90477)

    Zebrafish

    Myoblast determination protein 1 homolog

    May act as a transcriptional activator that promotes transcription of muscle-specific target genes and plays a role in muscle differentiation

    Similar to 1

7. Q8IU24_BRABE (Q8IU24)

    Amphioxus (Amphioxi are small marine animals found widely in the coastal waters of the warmer parts of the world)

    MyoD-related

    Not much information. Does not say that it does muscle differentiation.

8. MYOD_DROME (P22816)

    Fruit fly

    Myogenic-determination protein

    May play an important role in the early development of muscle.

    Does not say that it causes muscle differentiation.

9. LIN32_CAEEL (Q10574)

    C Elegans

    Essential for the specification of the neuroblast cell fate in the development of peripheral sense organs.

    neuroblast :a neuroblast or primitive nerve cell is a postmitotic cell that does not divide further, and which will develop into a neuron after a migration phase.

    looks like a gene involved in cell differentiation but not muscle cells. Might have some similarity with others too.

10. SYFM_HUMAN (O95363)

    Homo sapiens (Human)

    Phenylalanine--tRNA ligase, mitochondrial

    Is responsible for the charging of tRNA(Phe) with phenylalanine in mitochondrial translation.

    Present in chromosome 6 of human DNA

    phenylalanine - An essential amino acid, C9H11NO2, that occurs as a constituent of many proteins and is converted to tyrosine in the body.

    tRNA -  any of a class of small, cloverleaf forms of RNA that transfer unattached amino acids in the cell cytoplasm to the ribosomes for protein synthesis.

    Mitochondrial translation is responsible for the maintenance of the cellular energetic balance through synthesis of proteins involved in oxidative phosphorylation. 

    Mitochondrial translation is specifically defined as the process within mitochondria whereby mitochondrial mRNA (mt-mRNA) is translated by mitochondrial ribosomes (mitoribosomes) to generate an amino acid polypeptide.

    This is completely separate from other proteins as it helps in attaching amino acid to t-RNA



## Running code

    python run.py --seq1 MELLSLCSWFAAATTYDADFYDDP --seq2 MSNWTATSSDSTS --permutations 10
    python run.py --seq1 deadly --seq2 ddgearlyk --permutations 999
    python run_all_proteins.py
    python run.py --seq1 proteins/P15172.fasta --seq2 proteins/Q10574.fasta --permutations 999
    python run.py --seq1 proteins/P15172.fasta --seq2 proteins/O95363.fasta --permutations 999