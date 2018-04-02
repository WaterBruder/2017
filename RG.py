#分类和预测：
class ModelAndFacst():
    def __init__(self,data):
        self.data=data



#回归分析

#线性回归

#特征消除
    def Rlr(self,xcs,ycs):
        x=self.data[xcs].as_matrix()
        y=self.data[ycs].as_matrix()
        from sklearn.linear_model import RandomizedLogisticRegression as RLR
        rlr=RLR()#selection_threshol
        rlr.fit(x,y)
        x=self.data[self.data[xcs].columns[rlr.get_support()]].as_matrix()
        return (x,y)



    # 在随机Lasso和随机逻辑回归中有对稳定性选择的实现
    def logic_classify(self,xcs,ycs):
        from sklearn.linear_model import LogisticRegression as LR
        lr=LR()
        x1,y1=self.Rlr(xcs,ycs)
        if 0 in x1.shape:
            print ("特征消除失败")
        else:
            lr.fit(x1,y1)
            if lr.score(x1,y1)>=0.80:
                 print (lr.coef_)
            else:
                 print("logic回归准确性不足")


#非线性回归


#Logistic回归


#岭回归


#主成分回归


#偏最小二乘回归


#决策树
    def decision_making_tree(self,xcs,ycs):
        x=self.data[xcs].astype(int)
        y=self.data[ycs].astype(int)
        from sklearn.tree import DecisionTreeClassifier as DTC
        dtc=DTC(criterion='entropy')
        dtc.fit(x,y)
        from sklearn.tree import export_graphviz
        from sklearn.externals.six import StringIO
        with open("tree.dot",'w') as f:
            f=export_graphviz(dtc,feature_names=x.columns,out_file=f)




#人工神经网络
#BP神经网络
    def neural_network(self,xcs,ycs,a,b,c,d,e,f):
        x=self.data[xcs].astype(int)
        y=self.data[ycs].astype(int)
        from keras.models import Sequential
        from keras.layers.core import Dense,Activation
        model=Sequential()
        model.add(Dense(a,b))
        model.add(Activation(d))
        model.add(Dense(b,c))
        model.add(Activation(e))

        model.compile(loss='binary_crossentropy',optimizer='adam',class_mode='binary')
        model.fit(x,y,nb_epoch=f,batch_size=d)
        yp=model.predict_classes(x),reshape(len(y))

        self.cm_plot(y,yp).show()


    def cm_plot(self, y, yp):

        from sklearn.metrics import confusion_matrix  # 导入混淆矩阵函数

        cm = confusion_matrix(y, yp)  # 混淆矩阵

        import matplotlib.pyplot as plt  # 导入作图库
        plt.matshow(cm, cmap=plt.cm.Greens)  # 画混淆矩阵图，配色风格使用cm.Greens，更多风格请参考官网。
        plt.colorbar()  # 颜色标签

        for x in range(len(cm)):  # 数据标签
            for y in range(len(cm)):
                plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')

        plt.ylabel('True label')  # 坐标轴标签
        plt.xlabel('Predicted label')  # 坐标轴标签
        return plt

    #Apriori
    # 自定义连接函数，用于实现L_{k-1}到C_k的连接
    def connect_string(self,x, ms):
        x = list(map(lambda i: sorted(i.split(ms)), x))
        l = len(x[0])
        r = []
        for i in range(len(x)):
            for j in range(i, len(x)):
                if x[i][:l - 1] == x[j][:l - 1] and x[i][l - 1] != x[j][l - 1]:
                    r.append(x[i][:l - 1] + sorted([x[j][l - 1], x[i][l - 1]]))
        return r

    # 寻找关联规则的函数
    def find_rule(self,d, support, confidence, ms=u'--'):
        result = pd.DataFrame(index=['support', 'confidence'])  # 定义输出结果

        support_series = 1.0 * d.sum() / len(d)  # 支持度序列
        column = list(support_series[support_series > support].index)  # 初步根据支持度筛选
        k = 0

        while len(column) > 1:
            k = k + 1
            print(u'\n正在进行第%s次搜索...' % k)
            column = self.connect_string(column, ms)
            print(u'数目：%s...' % len(column))
            sf = lambda i: d[i].prod(axis=1, numeric_only=True)  # 新一批支持度的计算函数

            # 创建连接数据，这一步耗时、耗内存最严重。当数据集较大时，可以考虑并行运算优化。
            d_2 = pd.DataFrame(list(map(sf, column)), index=[ms.join(i) for i in column]).T

            support_series_2 = 1.0 * d_2[[ms.join(i) for i in column]].sum() / len(d)  # 计算连接后的支持度
            column = list(support_series_2[support_series_2 > support].index)  # 新一轮支持度筛选
            support_series = support_series.append(support_series_2)
            column2 = []

            for i in column:  # 遍历可能的推理，如{A,B,C}究竟是A+B-->C还是B+C-->A还是C+A-->B？
                i = i.split(ms)
                for j in range(len(i)):
                    column2.append(i[:j] + i[j + 1:] + i[j:j + 1])

            cofidence_series = pd.Series(index=[ms.join(i) for i in column2])  # 定义置信度序列

            for i in column2:  # 计算置信度序列
                cofidence_series[ms.join(i)] = support_series[ms.join(sorted(i))] / support_series[
                    ms.join(i[:len(i) - 1])]

            for i in cofidence_series[cofidence_series > confidence].index:  # 置信度筛选
                result[i] = 0.0
                result[i]['confidence'] = cofidence_series[i]
                result[i]['support'] = support_series[ms.join(sorted(i.split(ms)))]

        result = result.T.sort(['confidence', 'support'], ascending=False)  # 结果整理，输出
        print(u'\n结果为：')
        print(result)

        return result

    def Apriori(self,cs,st,cd,outputfile):
        csdata=self.data[cs]
        ct= lambda x: pd.Series(1,index=x[pd.notnull(x)])
        b=map(ct,data.as_matrix())
        data=pd.DataFrame(list(b),fillna(0))
        del b
        support=st
        confidence=cd
        ms='---'
        self.find_rule(data,support,confidence,ms).to_excel(outputfile)





#贝叶斯网络



#支持向量机



#时序模式 :平滑法 趋势拟合法 组合模型法 AR模型 MA模型 ARMA模型 ARIMA模型 ARCH模型 CARCH 模型

    def ARIMA(self,index_name,cn):
        self.data.set_index(index_name)
        self.data=self.data[cn]
        import matplotlib.pyplot as plt
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        self.data.plot()
        plt.show()

        # 自相关图
        from statsmodels.graphics.tsaplots import plot_acf
        plot_acf(self.data).show()

        # 平稳性检测
        from statsmodels.tsa.stattools import adfuller as ADF
        print(u'原始序列的ADF检验结果为：', ADF(self.data[cn]))
        # 返回值依次为adf、pvalue、usedlag、nobs、critical values、icbest、regresults、resstore

        # 差分后的结果
        D_data = self.data.diff().dropna()
        D_data.columns = ('差分%s' % cn)
        D_data.plot()  # 时序图
        plt.show()
        plot_acf(D_data).show()  # 自相关图
        from statsmodels.graphics.tsaplots import plot_pacf
        plot_pacf(D_data).show()  # 偏自相关图
        print(u'差分序列的ADF检验结果为：', ADF(D_data[D_data.columns]))  # 平稳性检测

        # 白噪声检验
        from statsmodels.stats.diagnostic import acorr_ljungbox
        print(u'差分序列的白噪声检验结果为：', acorr_ljungbox(D_data, lags=1))  # 返回统计量和p值

        from statsmodels.tsa.arima_model import ARIMA

        data[cn] = data[cn].astype(float)
        # 定阶
        pmax = int(len(D_data) / 10)  # 一般阶数不超过length/10
        qmax = int(len(D_data) / 10)  # 一般阶数不超过length/10
        bic_matrix = []  # bic矩阵
        for p in range(pmax + 1):
            tmp = []
            for q in range(qmax + 1):
                try:  # 存在部分报错，所以用try来跳过报错。
                    tmp.append(ARIMA(self.data, (p, 1, q)).fit().bic)
                except:
                    tmp.append(None)
            bic_matrix.append(tmp)

        bic_matrix = pd.DataFrame(bic_matrix)  # 从中可以找出最小值

        p, q = bic_matrix.stack().idxmin()  # 先用stack展平，然后用idxmin找出最小值位置。
        print(u'BIC最小的p值和q值为：%s、%s' % (p, q))
        model = ARIMA(self.data, (p, 1, q)).fit()  # 建立ARIMA(0, 1, 1)模型
        model.summary2()  # 给出一份模型报告
        model.forecast(5)  # 作为期5天的预测，返回预测结果、标准误差、置信区间。
