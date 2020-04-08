# coding:utf-8import pandas as pdimport numpy as npimport osimport matplotlib.pyplot as pltfrom sklearn import preprocessingfrom sklearn.datasets import make_blobsfrom sklearn.datasets import make_classificationfrom sklearn import metricsfrom sklearn.cluster import KMeans#让中文显示正常plt.rcParams['font.sans-serif']=['Microsoft YaHei'] #用来正常显示中文标签字体。Microsoft YaHei 或 SimHeiplt.rcParams['axes.unicode_minus']=False #用来正常显示负号PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))path = os.path.join(PROJECT_ROOT,'02-26围观.xlsx')df = pd.read_excel(path)print (df)'''训练数据进行标准化/归一化/正则化，为什么呢？1）去除量纲的影响，将有量纲的数值变成无量纲的纯数值；2）是去除各特征之间数值差异过大的问题，比如一个向量（uv:10000, rate:0.03,money: 20)，如果要与其它向量一起计算欧氏距离或者余弦相似度时，会向uv倾斜非常严重，导致其余2个特征对模型的贡献度非常低3）提升训练的速度，防止过拟合n_samples:待生成的样本的总数n_features:每个样本的特征数,默认为2centers: 要生成的样本中心（类别）数，默认为3cluster_std: 每个类别的方差，默认为1shuffle: 打乱 (default=True)sklearn1)n_clusters: K值，这个值一般需要结合第3点的评判标准，找到最佳的K2）max_iter： 最大的迭代次数，一般如果是凸数据集的话可以不管这个值，如果数据集不是凸的，可能很难收敛，此时可以指定最大的迭代次数让算法可以及时退出循环。3）n_init：用不同的初始化质心运行算法的次数。由于K-Means是结果受初始值影响的局部最优的迭代算法，因此需要多跑几次以选择一个较好的聚类效果，默认是10，一般不需要改。如果你的k值较大，则可以适当增大这个值。4）init： 初始值选择的方式，一般默认’k-means++’。'''x,y = make_blobs(n_samples=1000,n_features=2,centers=4,cluster_std=[0.2,0.3,0.5,0.4],shuffle=True,random_state=9)print (x)print (x[:5])print (y)score = []fig = plt.figure(figsize=(20,20))ax1 = fig.add_subplot(221)plt.scatter(x[:,0],x[:,1],c=y)plt.title('原始（设定分4类）')ax2 = fig.add_subplot(222)clf = KMeans(n_clusters=3,max_iter=1000)pred = clf.fit_predict(x)score.append(metrics.calinski_harabaz_score(x,pred))plt.scatter(x[:,0],x[:,1],c=pred)plt.title('Kmeans分3类')ax3 = fig.add_subplot(223)clf = KMeans(n_clusters=4,max_iter=1000)pred = clf.fit_predict(x)score.append(metrics.calinski_harabaz_score(x,pred))plt.scatter(x[:,0],x[:,1],c=pred)plt.title('Kmeans分4类')ax4 = fig.add_subplot(224)clf = KMeans(n_clusters=6,max_iter=1000)pred = clf.fit_predict(x)score.append(metrics.calinski_harabaz_score(x,pred))plt.scatter(x[:,0],x[:,1],c=pred)plt.title('Kmeans分6类')plt.show()print (score)