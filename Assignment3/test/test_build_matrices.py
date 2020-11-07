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

