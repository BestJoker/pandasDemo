# coding:utf-8import pandas as pdimport numpy as npimport osimport matplotlib.pyplot as pltimport scipy.stats as stimport mathimport seaborn as snsfrom time import timeimport datetimeimport model_test_indexfrom sklearn.model_selection import train_test_splitfrom sklearn.linear_model import LogisticRegressionfrom sklearn.ensemble import RandomForestClassifierpd.options.mode.chained_assignment = None # 默认是'warn'plt.rcParams['font.sans-serif']=['Microsoft YaHei'] #用来正常显示中文标签字体。Microsoft YaHei 或 SimHeiplt.rcParams['axes.unicode_minus']=False #用来正常显示负号#获取文件路径def get_file_path(file_name):    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))    path = os.path.join(PROJECT_ROOT, 'data/' + file_name)    return path#对于空缺值进行填补def fillna_vacancy_value(orign_df):    str_columns = orign_df.select_dtypes(include=['object', 'datetime']).columns    num_columns = orign_df.select_dtypes(include=['number']).columns    orign_df[str_columns] = orign_df[str_columns].fillna('')    orign_df[num_columns] = orign_df[num_columns].fillna(value=0)    return orign_df#获取原始数据def get_orign_data():    file_name = '需求-#396 新注册用户7日转化模型探索.xlsx'    path = get_file_path(file_name)    # 获取训练数据    train_df = pd.read_excel(path, sheet_name=u'训练数据')    train_df = fillna_vacancy_value(train_df)    # 获取预测数据    target_df = pd.read_excel(path, sheet_name=u'预测数据')    target_df = fillna_vacancy_value(target_df)    print (train_df.shape, target_df.shape)    return train_df,target_df# 元数据处理# 输入：原始df# 输出：参与算法的df，标准化的X，对应的ydef handle_data(df):    # 获取目标参数    columns = [        '是否支付',        '总看课时长(min)',        '总H5+小程序活跃次数',        '分享次数',        '课表访问次数',        '支付页面访问次数'    ]    temp_df = df[columns]    # 获取因变量和自变量    X = temp_df.iloc[:, temp_df.columns != '是否支付']    y = temp_df.iloc[:, temp_df.columns == '是否支付'].values.ravel()    # 标准化    from sklearn.preprocessing import StandardScaler    scaler = StandardScaler()  # 实例化    X_standar = scaler.fit_transform(X)    return temp_df, X, y#获取基础模型数据def get_baseModel_info(model_type, X_standar, y,is_evolve=0):    print ('进行' + model_type + '运行')    X_train, X_test, Y_train, Y_test = train_test_split(X_standar, y, test_size=0.3, random_state=420)    # 逻辑回归    if model_type == 'LR':        if is_evolve == 1:            #优化之后            L1 = LogisticRegression(penalty='l1', solver='liblinear', C=0.012895, max_iter=1000,                                    class_weight='balanced')        else:            #基础水准            L1 = LogisticRegression(penalty='l1', solver='liblinear', C=0.012895, max_iter=1000,                                    class_weight='balanced')            # 测试数据            # 模型准确率: 81.91 %            # 模型精确率: 3.39 %            # 模型召回率: 70.59 %            # 模型F1值: 6.47 %            # 真实数据            # 模型准确率: 85.48 %            # 模型精确率: 2.39 %            # 模型召回率: 69.09 %            # 模型F1值: 4.61 %    # 随机森林    elif model_type == 'RFC':        if is_evolve == 1:            #优化之后            L1 = RandomForestClassifier(n_estimators=17, max_depth=4, min_samples_leaf=22, min_samples_split=11,                                        max_features=4, class_weight='balanced')        else:            #基础水准            L1 = RandomForestClassifier(n_estimators=20,max_depth=4, class_weight='balanced')    else:        return '错误模型'    L1 = L1.fit(X_train, Y_train)    y_predcit = L1.predict(X_test)    model_test_index.basic_data_confusion(Y_test, y_predcit)    y_predprob = L1.predict_proba(X_test)    model_test_index.auc_roc_curve(Y_test, y_predprob)    return L1#训练模型找最优参数def train_model_method(X_standar,y):    result_df = pd.DataFrame()    for c in np.linspace(0.005,0.02,20):    # for c in np.arange(2, 7, 1):        print (c)        # 训练模型        X_train, X_test, Y_train, Y_test = train_test_split(X_standar, y, test_size=0.3, random_state=420)        L1 = LogisticRegression(penalty='l1', solver='liblinear', C=c, max_iter=1000,                                    class_weight='balanced')        L1 = L1.fit(X_train, Y_train)        y_predcit = L1.predict(X_test)        accuracy_score_l, precision_score_l, recall_score_l, f1_score_l = model_test_index.basic_data_confusion(Y_test,                                                                                                                y_predcit,                                                                                                                report=False,                                                                                                                draw_pic=False,                                                                                                                log=False)        temp_df = pd.DataFrame([{            'c值': c,            '模型准确率': accuracy_score_l,            '模型精确率': precision_score_l,            '模型召回率': recall_score_l,            '模型F1值': f1_score_l        }])        result_df = pd.concat([result_df, temp_df], axis=0)    result_df = result_df.reset_index()    return result_df#真实数据模型预测def real_predict_method(model):    # 预测数据    target_handle_df, orign_predict_X_standar, orign_predict_y = handle_data(target_df)    print (target_handle_df.shape)    y_predcit = model.predict(orign_predict_X_standar)    model_test_index.basic_data_confusion(orign_predict_y, y_predcit)    y_predprob = model.predict_proba(orign_predict_X_standar)    model_test_index.auc_roc_curve(orign_predict_y, y_predprob)    return y_predcit#主函数if __name__ == '__main__':    train_df,target_df = get_orign_data()    print (train_df.head())    print (target_df.head())    # 获取训练数据    train_handle_df, train_X_standar, train_y = handle_data(train_df)    RFC_model = get_baseModel_info('RFC', train_X_standar, train_y)    print ('-'*40)    # 模型调优    # result_df = train_model_method(train_X_standar, train_y)    # print (result_df)    # 预测真实值    real_predict_method(RFC_model)