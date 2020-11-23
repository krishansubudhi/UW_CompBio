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

##  optional

1. Jupyter notebook
    
    If familiar with jupyter notebooks, run

        jupyter notebook
    Open `evaluate.ipynb` and run all cells.

2. Debugging

    For debuggin on a smaller sequence, modify these lines in `run.py`

        sequence = sequence_all[:<desired_length>]
        total_iter = <desired_num_iterations>