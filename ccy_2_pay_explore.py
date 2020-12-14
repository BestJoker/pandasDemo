# coding:utf-8import pandas as pdimport numpy as npimport osimport matplotlib.pyplot as pltimport scipy.stats as stimport mathimport seaborn as snsfrom sklearn.preprocessing import OneHotEncoderimport model_test_indexfrom sklearn.preprocessing import StandardScalerfrom sklearn.model_selection import GridSearchCVfrom sklearn.model_selection import train_test_splitfrom sklearn.metrics import accuracy_scorefrom sklearn.model_selection import cross_val_scorefrom sklearn.neighbors import KNeighborsClassifierfrom sklearn.discriminant_analysis import LinearDiscriminantAnalysisfrom sklearn.naive_bayes import GaussianNBfrom sklearn.svm import SVCfrom sklearn.linear_model import LogisticRegressionfrom sklearn.tree import DecisionTreeClassifierfrom sklearn.model_selection import KFoldfrom sklearn.ensemble import RandomForestClassifierpd.options.mode.chained_assignment = None # 默认是'warn'plt.rcParams['font.sans-serif']=['Microsoft YaHei'] #用来正常显示中文标签字体。Microsoft YaHei 或 SimHeiplt.rcParams['axes.unicode_minus']=False #用来正常显示负号#第一轮初步筛选寻找高相关参数def first_choice(orign_df):    columns = [        'live_course_counts',        'is_in_group',        'regist_now_days',        'sum_duration_min',        'is_pay',        'has_watch_live',        'sum_12_7_duration_min',        'sum_12_1_duration_min',        'schdule_counts',        'share_times',        'live_share_times',        'before_ccy_7_daus',        'ccy_dur_daus',        '看直播数量(int)',        '看直播时长(min)',        '看直播课的回放时长(min)',        '非转化营直播课程的看课时长(min)',        '理论课时长(min)',        '前沿课时长(min)',        '理论课看课数量',        '前沿课看课数量'    ]    temp_df = orign_df[orign_df['user_status_type']=='9.9冲刺营']    temp_df = temp_df[columns]    temp_df['is_in_group'] = temp_df['is_in_group'].map({        '不在群里':0,        '在群里':1    })    a = temp_df.corr()    f, ax = plt.subplots(figsize=(20, 20), dpi=180)    # 调色板ma    cmap = sns.diverging_palette(220, 10, as_cmap=True)    sns.heatmap(a, ax=ax, square=True, lw=0.3, cmap=cmap, annot=True)    ax.set_title('相关系数矩阵', fontsize=20)    plt.show()    #筛选出来的有用的指标为：    #schdule_counts    #share_times，live_share_times，二者取其一    #before_ccy_7_daus    #ccy_dur_daus    #看直播数量(int)，看直播时长(min)，二者取其一    #非转化营直播课程的看课时长(min)，前沿课时长(min)，二者取其一    #理论课时长(min)    #is_in_group:可能因为分类问题导致相关性不强，但是我们带上def base_KNN(x,y):    X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=0.3,random_state=420)    knn = KNeighborsClassifier(n_neighbors=5,weights="uniform")    knn = knn.fit(X_train,Y_train)    y_predict = knn.predict(X_test)    model_test_index.basic_data_confusion(Y_test,y_predict)    y_preprob = knn.predict_proba(X_test)    model_test_index.auc_roc_curve(Y_test,y_preprob)    model_test_index.corss_val_score_cus(knn,x,y,cv=5)    print ('-' * 30)    # base:  调参无效    # 模型准确率: 97.73 %    # 模型精确率: 57.14 %    # 模型召回率: 11.76 %    # 模型F1值: 19.51 %    # AUC值为： 63.41 %    # param_grid = {    #     'weights': ['uniform','distance'],    #     'n_neighbors': range(1, 20)    # }    #    # knn = KNeighborsClassifier()    # GS = GridSearchCV(knn, param_grid, cv=10)    # GS.fit(x, y)    #    # print (GS.best_params_) #{'n_neighbors': 5, 'weights': 'uniform'}    # print (GS.best_score_) #0.9753826587961744def base_LR(x,y):    X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=0.3,random_state=420)    L1 = LogisticRegression(penalty='l1', solver='saga', C=0.05, max_iter=1000, class_weight='balanced')    L1 = L1.fit(X_train, Y_train)    y_predcit = L1.predict(X_test)    model_test_index.basic_data_confusion(Y_test, y_predcit)    y_predprob = L1.predict_proba(X_test)    model_test_index.auc_roc_curve(Y_test, y_predprob)    print ('-'*30)    # 模型准确率: 81.32 %    # 模型精确率: 7.53 %    # 模型召回率: 61.76 %    # 模型F1值: 13.42 %    # AUC值为： 82.35 %def iteration_LR(x,y):    param_grid = {        'penalty': ['l1', 'l2'],        'solver': ['liblinear','saga'],        'C': np.arange(0.1,1,0.1),        'class_weight':['balanced'],        'max_iter':range(300,1000,200)    }    lr = LogisticRegression()    GS = GridSearchCV(lr, param_grid, cv=10)    GS.fit(x, y)    print (GS.best_params_) #    print (GS.best_score_) #def base_RFC(x,y):    rfc = RandomForestClassifier(n_estimators=41,criterion='gini',max_depth=9,random_state=420,class_weight="balanced",n_jobs=-1)    X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=0.3,random_state=420)    rfc = rfc.fit(X_train,Y_train)    y_predict = rfc.predict(X_test)    model_test_index.basic_data_confusion(Y_test,y_predict)    y_preprob = rfc.predict_proba(X_test)    model_test_index.auc_roc_curve(Y_test,y_preprob)    model_test_index.corss_val_score_cus(rfc,x,y,cv=5)    # joblib.dump(rfc,get_file_path('rfc.pkl'))    return rfc#初步探索选择模型def data_handel(orign_df):    temp_df = orign_df.copy(deep=True)    columns = [        'schdule_counts',        'share_times',        'before_ccy_7_daus',        'ccy_dur_daus',        '看直播时长(min)',        '非转化营直播课程的看课时长(min)',        '理论课时长(min)',        'is_pay',        'is_in_group'    ]    temp_df = temp_df[columns]    #调整is_in_group的分类    season_dummy = pd.get_dummies(temp_df['is_in_group'],prefix='is_in_group')    temp_df = pd.concat([temp_df,pd.DataFrame(season_dummy)],axis=1)    temp_df.drop(['is_in_group'],axis=1,inplace=True)    #数据标准化    X = temp_df[['看直播时长(min)','非转化营直播课程的看课时长(min)','理论课时长(min)']].values    scaler = StandardScaler()  # 实例化    x_std = scaler.fit_transform(X)    temp_df[['看直播时长(min)', '非转化营直播课程的看课时长(min)', '理论课时长(min)']] = x_std    X = temp_df.iloc[:, temp_df.columns != 'is_pay']    y = temp_df['is_pay']    print ('-'*30)    iteration_LR(X,y)    # choice_model(X,y)    # KNN:0.974966 (0.011124)    # LR:0.974138 (0.010404)    # SVM:0.974345 (0.009981)    # RFC:0.973724 (0.010274)def choice_model(x,y):    # prepare models    models = []    models.append(('LR', LogisticRegression()))    models.append(('LDA', LinearDiscriminantAnalysis()))    models.append(('KNN', KNeighborsClassifier()))    models.append(('CART', DecisionTreeClassifier()))    models.append(('NB', GaussianNB()))    models.append(('SVM', SVC()))    models.append(('RFC',RandomForestClassifier()))    # evaluate each model in turn    results = []    names = []    scoring = 'accuracy'    for name, model in models:        kfold = KFold(n_splits=10, random_state=7)        cv_results = cross_val_score(model, x, y, cv=kfold, scoring=scoring)        results.append(cv_results)        names.append(name)        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())        print(msg)    # boxplot algorithm comparison    fig = plt.figure()    fig.suptitle('Algorithm Comparison')    ax = fig.add_subplot(111)    plt.boxplot(results)    ax.set_xticklabels(names)    plt.show()    # choice_model(X,y)    # KNN:0.974966 (0.011124)    # LR:0.974138 (0.010404)    # SVM:0.974345 (0.009981)    # RFC:0.973724 (0.010274)#主函数if __name__ == '__main__':    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))    path = os.path.join(PROJECT_ROOT,'data/认知进化营同学明细数据-英文版.xlsx')    orign_df = pd.read_excel(path)    str_columns = orign_df.select_dtypes(include=['object', 'datetime']).columns    num_columns = orign_df.select_dtypes(include=['number']).columns    orign_df[str_columns] = orign_df[str_columns].fillna('')    orign_df[num_columns] = orign_df[num_columns].fillna(value=0)    orign_df.info()    # first_choice(orign_df)    data_handel(orign_df)