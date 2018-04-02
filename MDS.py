
def datadelete(data,): #平滑噪声数据
    pass

class MissingValueAndOutlier():
    def __init__(self,data):
        self.data=data;

    def datadelete(self,delete_name, axis=1):  # 删除数据
        self.data = self.data.drop(delete_name, axis)
        print (self.data)

    def Mean(self,colunms):#平均值补充缺失值
        for column_no in colunms:
            mean=self.data[column_no].mean()
            for i in range(len(self.data[column_no])):
              if (self.data[column_no].isnull()[i]):
                 self.data[column_no][i]=mean

    def Median(self,colunms):#中位数补充缺失值
        for column_no in colunms:
            median=self.data[column_no].median()
            for i in range(len(self.data[column_no])):
              if (self.data[column_no].isnull()[i]):
                 self.data[column_no][i]=median

    def manual(self,column_name,want_value):#手工补充缺失值
        for i in range(len(self.data[column_name])):
            if (self.data[column_name].isnull()[i]):
                self.data[column_name][i]=want_value

    def lagrange(self,columns):#lagrange插值
        from scipy.interpolate import lagrange
        for column_no in columns:
            for i in range(len(self.data[column_no])):
              if (self.data[column_no].isnull()[i]):
                 self.data[column_no][i]=ployinterp_column(self.data[column_no],i,k=5)

    def ployinterp_column(self,s, n, k=5):
         y = s[list(range(n-k, n)) + list(range(n+1, n+1+k))]
         y = y[y.notnull()]
         return lagrange(y.index, list(y))(n)

    def IsOutlier(self,columns_name,max_factor=1.5,min_factor=1.5): #清理异常值
        lol=self.data[columns_name].describe()
        minvalue = lol['25%']- min_factor * (lol['75%'] - lol['25%'])
        maxvalue = lol['75%'] + max_factor* (lol['75%'] - lol['25%'])
        for i in range(len(self.data[columns_name])):
            if (self.data[columns_name][i]>maxvalue)or(self.data[columns_name][i]<minvaue):
                self.data[columns_name][i]=NAN

#数据集成 实体识别：同名异义 异名同义 单位不统一
#        冗余属性识别 同一属性多次出现 同一属性命名不一致导致重复





