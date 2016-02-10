import math
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np


class Bunch(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


def selected_features(X_all, X, features):
    """
    after transform() was run on X_all and X is the result
    find the name of features that got selected
    
    extract columns from X
    compare to columns in X_all
    read the name of features in X_all
    """
    selected_features = []
    for x_col in range(X.shape[1]):
        for col in range(X_all.shape[1]):
            if np.array_equal(X_all[:,col], X[:,x_col]):
                selected_features.append(features[col])
    return selected_features


def plot_grid(df, features, logy=True):
    grid_columns = 4
    grid_rows = int(math.ceil(len(features) / float(grid_columns)))
    
    fig = figure()
    fig.set_size_inches(14, 3.5*grid_rows)
    ax = list()

    for row in range(0, grid_rows):
        for column in range(0, grid_columns):
            if row*grid_columns + column < len(features):
                ax.append(plt.subplot2grid((grid_rows, grid_columns), (row, column)))

    for ix, feature in enumerate(features):
        df[feature].value_counts().sort_index().plot('bar', ax=ax[ix], title=feature, alpha=0.8, logy=logy)

    plt.tight_layout()
    plt.show()
    plt.close()


def get_first_with_label(X, lb):
    """
    there are two columns with the same label
        take the first of them
    """
    return X[lb].iloc[:,:1]


def plot_roc(y_test, y_score):
    from sklearn.metrics import roc_curve, auc

    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)

    plt.figure()

    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")

    plt.show()
    plt.close()


def plot_confusion_matrix(y_test, y_score):
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y_test, y_score)

    plt.matshow(cm)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    plt.show()
    plt.close()


def print_performance_metrics(cm):
    """
    binary confusion matrix
    """
    TN = cm[0,0]
    FP = cm[0,1]
    FN = cm[1,0]
    TP = cm[1,1]

    P = TP + FN
    N = FP + TN
    P_hat = TP + FP
    N_hat = FN + TN

    print "Precision = %f" % (TP / P_hat)
    print "Type I = %f" % (FP / N)
    print "Sensitivity = %f" % (TP / P)
    print "Type II = %f" % (FN / P)
    print "Recall = %f" % (1 - (FN / P))
    print "Specificity = %f" % (TN / N)
    print "Accuracy = %f" % ((TP + TN) / (P + N))
