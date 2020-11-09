from assignment3.roc import *
def test_roc():
    y_true = [     0,   1,   0, 0,    0,     1,  0,  1,    1,   1]
    y_score =[   -20, -10,   0, 0,   5,    50, 30,  10,    10,  100]
    roc = ROC(y_true, y_score)
    # roc.plot_roc()
    roc.calculateAUC()
    t = roc.largest_thres_TPR1()
    assert t ==-10
    TP, FP, TN, FN = roc.get_TP_FP_TN_FN(-10)
    assert TP == 5
    assert FP == 4
    assert TN == 1
    assert FN == 0

    TP, FP, TN, FN = roc.get_TP_FP_TN_FN(5)
    assert TP == 4
    assert FP == 2
    assert TN == 3
    assert FN == 1