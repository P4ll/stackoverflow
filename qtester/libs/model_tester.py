from sklearn.metrics import average_precision_score, mean_squared_error, roc_curve, auc, accuracy_score, classification_report, confusion_matrix, f1_score


def res_eval(goal, res, pos_labels=2):
    out = dict()
    out['class_rep'] = classification_report(goal, res)
    out['conf_matrix'] = confusion_matrix(goal, res)
    out['f1_score'] = f1_score(goal, res)

    fpr, tpr, thresholds = roc_curve(goal, res, pos_label=pos_labels)
    au_curve = auc(fpr, tpr)

    out['auc'] = au_curve
    return out