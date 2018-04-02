import numpy as np
import pandas as pd

class  data_standardization():
    def __init__(self,data):
        self.data=data

# 数据变换 对数据进行规范化
    def min_max(self,column_names):#最大_最小规范化
      for column_name in column_names:
        self.data[column_name]=self.data[column_name].astype('float64')
        min=self.data[column_name].min()
        max=self.data[column_name].max()
        chushu=max-min
        for i in range(len(self.data[column_name])):
                self.data[column_name][i]=(self.data[column_name][i]-min)/chushu
      print (self.data)

    def zero_mean(self,column_names):#零_均值规范化
      for column_name in column_names:
        self.data[column_name] = self.data[column_name].astype('float64')
        mean=self.data[column_name].mean()
        std=self.data[column_name].std()
        for i in range(len(self.data[column_name])):
                self.data[column_name][i]=(self.data[column_name][i]-mean)/std
      print(self.data)


    def decimal_scalling(self, column_names):  # 小数定标规范化
         for column_name in column_names:
             self.data[column_name] = self.data[column_name].astype('float64')
             for column_name in column_names:
                 for i in range(len(self.data[column_name])):
                     self.data[column_name][i] = self.data[column_name][i] / 10 ** np.ceil(
                         np.log10(self.data[column_name].abs().max()))
         print(self.data)

#连续属性离散化
#离散化：等宽 等频 基于聚类离散化

    def aequilate(self,column_names,k):
        for column_name in column_names:
            self.data[column_name]=pd.cut(self.data[column_name],k,labels=range(k))
        print(self.data)

    def equifrequent(self,column_names,k):
      for column_name in column_names:
        w=[1.0*i/k for i in range(k+1)]
        w=self.data[column_name].describe(percentiles=w)[4:4+k+1]
        w[0]=w.ix[0]*(1-(1e-10))
        self.data[column_name]=pd.cut(self.data[column_name],w,labels=range(k))
      print(self.data)

    def Kmeans(self,column_names,k,):
        from sklearn.cluster import KMeans
        for column_name in column_names:
          kmodel=KMeans(n_clusters=k,n_jobs=4)
          kmodel.fit(self.data[column_name].reshape(len(self.data[column_name]),1))
          c=pd.DataFrame(kmodel.cluster_centers_).sort_values(0)
          w=pd.rolling_mean(c,2).iloc[1:]
          w=[0]+list(w[0])+[self.data[column_name].max()]
          self.data[column_name]=pd.cut(self.data[column_name],w,labels=range(k))
        print(self.data)

     #属性构造
     #diy

    # 小波变换
    def xiaobobianhuan(self):
         pass


#属性规约：
     #合并属性 逐步向前选择 逐步向后删除 决策树归纳 主成分分析(前三种直接删除不相关维，后一种用于连续属性的数据降维)
    def pca(self,column_names):#主成分分析
         from sklearn.decomposition import PCA
         pca =PCA()
         pca.fit(self.data[column_names])
         pca.explained_variance_ratio_
         value=0
         i=0
         while(value<=0.95):
             value+=pca.explained_variance_ratio_[i]
             i+=1

         pca=PCA(i)
         pca.fit(self.data[column_names])
         low_d=pca.transform(self.data[column_names])
         self.data[column_names]=pd.DataFrame(low_d)
         print(self.data)
#数值规约
    #有参数方法：用一个模型评估数据，只需存放参数 回归和对数线性模型 无参数方法：需要存放实际数据，直方图 聚类 抽样
