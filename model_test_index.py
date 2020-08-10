# coding:utf-8from sklearn.model_selection import cross_val_scorefrom sklearn import metricsfrom sklearn.metrics import confusion_matrixfrom sklearn.metrics import accuracy_score, precision_score, recall_score, f1_scorefrom sklearn.metrics import classification_report #分类报告from sklearn.metrics import roc_auc_score, auc #ROC曲线import matplotlib.pyplot as pltimport seaborn as snsimport pandas as pdimport numpy as np#根据传入的y测试和y预测来输出准确率，精确率，召回率，F1值，以及绘制混淆矩阵,report是否打印报告#其中通常：y_pred = clf.predict(X_test)def basic_data_confusion(y_test,y_pred,report=True):    #计算混淆矩阵    conf_df = confusion_matrix(y_test, y_pred, labels=[0, 1])    # 绘制混淆矩阵    fig = plt.figure(figsize=(10, 5))    sns.heatmap(conf_df, annot=True, fmt='.20g', cmap=plt.cm.Blues)    plt.title('混淆矩阵', fontsize=20)    plt.xlabel('预测值', fontsize=15)    plt.ylabel('真实值', fontsize=15)    plt.show()    #基础数据指标    accuracy_score_l = accuracy_score(y_test, y_pred)    precision_score_l = precision_score(y_test, y_pred)    recall_score_l = recall_score(y_test, y_pred)    f1_score_l = f1_score(y_test, y_pred)    print("模型准确率:", '%.2f%%' % (accuracy_score_l * 100))    print("模型精确率:", '%.2f%%' % (precision_score_l * 100))    print("模型召回率:", '%.2f%%' % (recall_score_l * 100))    print("模型F1值:", '%.2f%%' % (f1_score_l * 100))    if report:        #分类报告        pd.set_option('display.max_rows', None)        print(classification_report(y_test, y_pred))    return accuracy_score_l,precision_score_l,recall_score_l,f1_score_l# 交叉验证def corss_val_score_cus(clf,X,y,cv,scoring='accuracy'):    clf_accuracy_scores = cross_val_score(clf, X, y, cv=cv, scoring=scoring)    print('基于{}折交叉验证的决策树模型准确率:{}'.format(cv,round(clf_accuracy_scores.mean(), 4)))    return clf_accuracy_scores# ROC曲线#y_predprob = rf0.predict_proba(X_test)def auc_roc_curve(y_test,y_probability):    #计算auc的值    fpr,tpr,thresholds = metrics.roc_curve(y_test,y_probability[:,1])    roc_auc = auc(fpr,tpr)    #开始绘制ROC曲线    plt.plot(fpr,tpr,'b',label='AUC = %0.2f'%roc_auc)    plt.legend(loc='lower right')    plt.plot([0,1],[0,1],'r--')    plt.xlim([-0.1,1.1])    plt.ylim([-0.1,1.1])    plt.xlabel('False Positive Rate') #横坐标是fpr    plt.ylabel('True Positive Rate') #纵坐标是tpr    plt.title('Receiver operating characteristic example')    plt.show()    print ('AUC值为：','%.2f%%'%(roc_auc*100))    return roc_auc