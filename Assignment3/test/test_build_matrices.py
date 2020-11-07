from assignment3.build_matrices import *

import unittest

def test_makeCountMatrix():
    s =  ['ACCGT', 'TACGG']
    matrix = makeCountMatrix(s)
    print(matrix)
    assert matrix.loc['A'][1] ==1
    assert matrix.loc['G'][4] ==2
    assert (matrix.sum(axis = 0) == 2).all()

def test_addPseudo():
    s =  ['ACCGT', 'TACGG']
    cm = makeCountMatrix(s)
    ps = addPseudo(cm, [1,2,3,4])
    print(ps)
    assert (ps.sum(axis = 0) == 2 + 10).all()

def test_makeFrequencyMatrix():
    s =  ['ACCGT', 'TACGG']
    cm = makeCountMatrix(s)
    fm = makeFrequencyMatrix(cm)
    print(fm)
    assert (fm.sum(axis = 0) == 1).all()
    assert fm.loc['A'][1] == 1/2

def test_entropy():
    fm = pd.DataFrame(
        [
            [0.625, 0,  0],
            [0,     0,  0],
            [0.25,  0,  1],
            [0.125, 1,  0]
        ],
    )
    e = entropy(fm, background = [0.25,0.25,0.25,0.25])
    assert round(e, 1) == 4.7 #0.625×1.32 -1× .125 + 1*2 + 1*2 # 1.32 is log likelihood of A in pos 1

def test_makeWMM():
    fm = pd.DataFrame(
        [
            [0.625, 0,  0],
            [0,     0,  0],
            [0.25,  0,  1],
            [0.125, 1,  0]
        ],
        index = list('ACGT'),
        columns = [1,2,3]
    )
    wmm = makeWMM(fm, background = [0.25,0.25,0.25,0.25])
    print(wmm)
    assert round(wmm.entropy, 1) == 4.7 
    assert round(wmm.loc['A'][1], 2) == 1.32
    assert wmm.loc['G'][1] == 0
    assert wmm.loc['T'][1] == -1 
    assert wmm.loc['T'][2] == 2

def test_scanWMM():
    wmm = pd.DataFrame(
        [
            [-36,   19,     1,  12, 10, -46],
            [-15,   -36,    -8, -9, -3, -31],
            [-13,   -46,    -6, -7, -9, -46],
            [17,    -31,    8,  -9, -6, 19]
        ],
        index = list('ACGT')
    )
    sequences = ['CTATAATC']
    scores = scanWMM(wmm, sequences)
    assert scores == [[-90,85,-91]]