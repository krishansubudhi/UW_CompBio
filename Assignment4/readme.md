## Build Instructions
This code is tested with `Python 3.8.0` on a Windows machine. Please install python verson 3.8 if facing library related errors. 

From the same directory containing `readme.md`,
1. Make sure data folder contains the `.fna` and `.gff` files. If not, download them and paste 

        ls data

        GCF_000091665.1_ASM9166v1_genomic.fna
        GCF_000091665.1_ASM9166v1_genomic.gff

2. Install Dependencies

        pip install -r requirements.txt

3. Run test cases

        python -m pytest .\test

4. Run viterbi training + evaluation

        python run.py

## Extra credit

To run the code for extra credit work do the following.
1. First run run.py as mentioned above which saves the hits to local directory.
2. Copy cached hit results to notebooks folder
        
        cp hits.pandas notebooks
3. Download and extract Methanocaldococcus_jannaschii_dsm_2661.ASM9166v1.46.gff3 from [this](ftp://ftp.ensemblgenomes.org/pub/bacteria/release-48/gff3/bacteria_0_collection/methanocaldococcus_jannaschii_dsm_2661) link.

        ls data

        GCF_000091665.1_ASM9166v1_genomic.fna
        GCF_000091665.1_ASM9166v1_genomic.gff
        Methanocaldococcus_jannaschii_dsm_2661.ASM9166v1.46.gff3
4. Start Jupyter

        jupyter notebook

5. Open `notebooks/extra.ipynb`. Run all cells

##  optional

1. Jupyter notebook
    
    If familiar with jupyter notebooks, run

        jupyter notebook
    Open `evaluate.ipynb` and run all cells.

2. Debugging

    For debuggin on a smaller sequence, modify these lines in `run.py`

        sequence = sequence_all[:<desired_length>]
        total_iter = <desired_num_iterations>