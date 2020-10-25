import numpy as np
import pandas as pd
import io
import re

def get_score_matrix(file :str):
    with open(file, 'r') as f:
        lines =  f.readlines()
    
    lines = [re.sub(' +',',',line.strip()) for line in lines if not line.startswith('#')]
    lines = '\n'.join(lines)
    buf = io.StringIO(lines)
    df = pd.read_csv(buf)
    return df.to_dict()