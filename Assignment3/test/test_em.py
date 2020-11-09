from assignment3.em import *

def test_Estep():
    wmm = pd.DataFrame(
        [
            [1, 2],
            [3, 0]
        ],
        index = list('AC')
    )
    background = [0.25, 0.25]
    sequences = ['ACA']

    expectations = Estep(wmm, sequences, background)
    # assert expectations.shape == (1,2)
    #AC
    expected_00 = np.power(2, 1) * background[0] * np.power(2, 0) * background[1]
    #CA . np power of wmm at pos and neucleotite (1,0) , (0,1)
    expected_01 = np.power(2, 3) * background[1] * np.power(2, 2) * background[0]
    
    print(expected_00, expected_01)
    s = expected_00 + expected_01
    expected_00 /= s
    expected_01 /= s
    assert expectations[0][0] ==  expected_00
    print(expectations)

def test_Mstep():
    E_zij = np.array(
        [
            [0, 1],
            [0, 1]
        ]
    )
    sequences = ['ACG', 'ACT']
    k = 2
    pseudocount = [1,1,1,1]
    background = 1,1,1,1

    wmm = Mstep(E_zij, sequences, k, pseudocount, background)
    assert wmm.loc['A'][1] == np.log2((0+1)/(2+4) /1) # 2 is total count at position 1. 4 is total pseudo counts. 1 is background
    print(wmm)