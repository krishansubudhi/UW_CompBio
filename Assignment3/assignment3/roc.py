from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np

class ROC:
    def __init__(self, y_true, y_score):
        self.y_true = y_true
        self.y_score = y_score
        self.fprs, self.tprs, self.thresholds = metrics.roc_curve(y_true, y_score)
    def plot_roc(self):
        plt.plot(self.fprs, self.tprs)
        plt.xlabel('FPR')
        plt.ylabel('TPR')
        plt.title('ROC curve')
        plt.show()

    def calculateAUC(self):
        auc = metrics.roc_auc_score(self.y_true, self.y_score)
        return auc
    
    def largest_thres_TPR1(self):
        thres_tpr1 = [t for tpr,t in zip(self.tprs, self.thresholds) if tpr == 1 ]
        return max(thres_tpr1)

    def get_TP_FP_TN_FN(self, threshold):
        for i,t in enumerate(self.thresholds):
            if t < threshold:
                break
            tpr, fpr = self.tprs[i], self.fprs[i]

        total  = len(self.y_true)
        P = np.array(self.y_true).sum()
        N = total - P
        tp = tpr * P
        fp = fpr * N
        fn = P - tp
        tn = N - fp

        return tp, fp, tn, fn