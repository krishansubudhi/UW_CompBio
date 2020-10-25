from assignment2.score import get_score_matrix

def test_get_score_matrix():
    score_matrix = get_score_matrix('blosum62.txt')
    assert list(score_matrix.keys()) == 'A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V'.split()
    assert list(score_matrix['A'].keys()) == 'A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V'.split()

    assert score_matrix['A']['A'] == 4
    assert score_matrix['A']['V'] == 0
    assert score_matrix['V']['V'] == 4
    assert score_matrix['E']['I'] == -3