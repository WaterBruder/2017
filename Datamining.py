import os
import sys
import pandas as pd
import re


def logo():
 print ("""
 #############################################################
 #                              | |~~~~~~~~~~~|======[***** |#
 #                              | |  MINING    \            |#
 #                              | |_____________\_______    |#
 #--Author : WasserBruder|Corn  | |==[ MDS ]============\   |#
 #--WECHATA: Solitaryjm         | |______________________\  |#
 #--Type   : DATA Mining        | \(@)(@)(@)(@)(@)(@)(@)/   |# 
 #--Version: 1.0.0              |  *********************    |#  
 #############################################################    
  """)


def usage():
    os.system('cls')
    logo()
    print("""
 +-----------------------------------------------------------------------+
 |                        DATA MINGING 详情介绍                          |
 +-----------------------------------------------------------------------+
 |本套工具用于数据预处理和挖掘建模。作者力在使数据分析的步骤简单化，提高效率，所以|
 |开发了这一套工具。开发过程中素材来源于作者数据分析实践中的各种案例所用的方法，作|
 |者尝试使这些方法一般化，以便于适合其他案例的数据。再者，工具架构简单，方便以后使|
 |用者根据自己的需要修改完善。目前工具鲁棒性不理想，功能也有待进一步完善，希望各位|
 |多多担待！                                                             |
 +------------------+----------------------------------------------------+
 |     Option       |                   Summary                          |
 +------------------+----------------------------------------------------+
 |1.用法介绍         |本套工具用法详细信息                               | 
 |2.数据清理         |删除数据、处理缺失值和异常值                       |
 |3.数据变换         |简单和规范化变换，离散化变换，小波变换             |
 |4.集成规约         |数据实体识别和规约、冗余属性识别和规约             |    
 |5.挖掘建模         |分类预测、聚类分析、关联规则、时序模式、离群点分析 |
 |6.数据保存         |数据保存                                           |
 +-----------------------------------------------------------------------+
 """)

def opendata(filepath,index_name=None):#从文件cvs or excel中读取数据
  layout=re.compile(r'\.(.*)').findall(filepath)[0]
  if layout=='xls' or layout=='xlsx':
    data=pd.read_excel(filepath,index=index_name)
  elif layout=='csv':
    data=pd.read_csv(filepath,encoding='gbk')
  else:
    print("wrong layout")

  return data


def data_cleaning(data_copy1):
    os.system('cls')
    import MDS
    handler = MDS.MissingValueAndOutlier(data_copy1)
    try:
        while (1):
            logo()
            print(""" 
    1.删除数据
    2.平均数补充缺失值
    3.中位数补充缺失值
    4.手工补充缺失值
    5.lagrange插值
    6.清理异常值
    7.数据集成

    其他任意键返回
    """)
            action = input('>>')
            if action == '1':
                cn = input('please input colunmn_name:')
                handler.datadelete(cn)

            elif action == '2':
                cs = input('please input column_names：')
                cs = cs.strip(',').split(',')  # 字符串转为列表
                handler.Mean(cs)

            elif action == '3':
                cs = input('please input column_names：')
                cs = cs.strip(',').split(',')  # 字符串转为列表
                handler.Median(cs)

            elif action == '4':
                cn = input('please input column_name:')
                wt = input('please input want_vlaue:')
                wt = int(wt)
                handler.manual(cn, wt)

            elif action == '5':
                cs = input('please input column_names：')
                cs = cs.strip(',').split(',')  # 字符串转为列表
                handler.lagrange(cs)

            elif action == '6':
                cn = input('please input column_name:')
                handler.IsOutlier(cn)

            else:
                return handler.data
    except KeyboardInterrupt:
        print("\n Critical. User aborted.")
        sys.exit(0)


def d_standardization(data_copy2):
    os.system('cls')
    import WC
    handler = WC.data_standardization(data_copy2)
    try:
        while (1):
            logo()
            print(""" 
    1.最大_最小规范化
    2.零_均值规范化
    3.小数定标规范化
    4.等宽离散化
    5.等频离散化
    6.K聚类离散化
    7.主成分分析

    其他任意键返回
    """)
            action = input('>>')
            if action == '1':
                cs = input('please input column_names：')
                cs = cs.strip(',').split(',')  # 字符串转为列表
                handler.min_max(cs)

            elif action == '2':
                cs = input('please input column_names：')
                cs = cs.strip(',').split(',')  # 字符串转为列表
                handler.zero_mean(cs)

            elif action == '3':
                cs = input('please input column_names：')
                cs = cs.strip(',').split(',')  # 字符串转为列表
                handler.decimal_scalling(cs)

            elif action == '4':
                cs = input('please input column_names:')
                cs = cs.strip(',').split(',')  # 字符串转为列表
                cn = input('please input class_number:')
                cn = int(cn)
                handler.aequilate(cs, cn)

            elif action == '5':
                cs = input('please input column_names:')
                cs = cs.strip(',').split(',')  # 字符串转为列表
                cn = input('please input class_number:')
                cn = int(cn)
                handler.equifrequent(cs, cn)

            elif action == '6':
                cs = input('please input column_names:')
                cs = cs.strip(',').split(',')  # 字符串转为列表
                cn = input('please input class_number:')
                cn = int(cn)
                handler.Kmeans(cs, cn)

            elif action=='7':
                cs = input('please input column_names：')
                cs = cs.strip(',').split(',')  # 字符串转为列表
                handler.pca(cs)

            else:
                return handler.data
    except KeyboardInterrupt:
        print("\n Critical. User aborted.")
        sys.exit(0)

def data_integration():
    print("""
    暂空
    """)

def Classification_modelingAndForecasting(data1):
    os.system('cls')
    import RG
    handler=RG.ModelAndFacst(data1)
    try:
        while (1):
            logo()
            print(""" 
    1.logic回归
    2.决策树
    3.BP
    4.Apriori
    5.ARIMA
    
    其他任意键返回
    """)
            action = input('>>')
            if action == '1':
                xcs = input('please input X_column_names：')
                xcs = xcs.strip(',').split(',')  # 字符串转为列表
                ycs = input('please input Y_column_names：')
                ycs = ycs.strip(',').split(',')
                handler.logic_classify(xcs, ycs)
            elif action=='2':
                xcs = input('please input X_column_names：')
                xcs = xcs.strip(',').split(',')  # 字符串转为列表
                ycs = input('please input Y_column_names：')
                ycs = ycs.strip(',').split(',')
                handler.decision_making_tree(xcs,ycs)
            elif action=='3':
                xcs = input('please input X_column_names：')
                xcs = xcs.strip(',').split(',')
                ycs = input('please input Y_column_names：')
                ycs = ycs.strip(',').split(',')
                a=input('please input input_node:')
                a=int(a)
                b=input('please input hidden_node:')
                b=int(b)
                d=input('please input output_node:')
                d=int(d)
                c=input('please input Activation1:')
                e=input('please input Activation2:')
                f=input('please input epoch:')
                f=int(f)
                handler.neural_network(xcs,ycs,a,b,c,d,e,f)
            elif action=='4':
                cs = input('please input column_names：')
                cs = xcs.strip(',').split(',')
                ct = input('please input support_value:')
                ct=float(ct)
                cd = input('please input confidentvalue:')
                cd=float(cd)
                outputfile=input('please input outputfile:')
                handler.Apriori(cs,st,cd,outputfile)
            elif action=='5':
                index_name=input('please input index_name:')
                cn=input('please input column_name:')
                handler.ARIMA(index_name,cn)
            else:
                return handler.data


    except KeyboardInterrupt:
        print("\n Critical. User aborted.")
        sys.exit(0)



def main():
  global ydata
  filepath = input("please input the filepath of data: ")
  # index_name=input("please input the index_name:")
  try:
        ydata = opendata(filepath)
  except:
        print("sorry,it can't read file")
        sys.exit(0)
  try:
    while True:
        logo()
        print("欢迎使用 DataeMining.请选择一个选项")
        print("""
            1.用法介绍  2.数据清理  3.数据变换
            4.集成规约  5.挖掘建模  6.数据保存
            """)
        action=input("\n>>") #返回都是字符串

        if action=='1':
            usage()

        elif action=='2':
            data_copy=ydata.copy()
            data_copy=data_cleaning(data_copy)
            cck=input("确认修改，请输入T:").upper()
            if cck=='t':
                ydata=data_copy
            else:
                print("不做修改")
                pass

        elif action=='3':
            data_copy=ydata.copy()
            data_copy=d_standardization(data_copy)
            cck=input("确认修改，请输入T:").upper()
            if cck=='t':
                ydata=data_copy
            else:
                print("不做修改")
                pass

        elif action=='4':
            data_integration()

        elif action=='5':
            Classification_modelingAndForecasting(ydata)

        elif action=='6':
                fp=input('please input the filepath you want to save data:')
                layout=re.compile(r'\.(.*)').findall(fp)[0]
                if layout =='xls' or layout =='xlsx':
                    try:
                        ydata.to_excel(fp)
                        print('save succeed')
                    except:
                        print('save failed')
                elif layout=='csv':
                    try:
                        ydata.to_csv(fp,encoding='gbk')
                        print('save succeed')
                    except:
                        print('save failed')
                else:
                    print('wrong layout')

        else:
            print("\n Critical. User aborted.")
            sys.exit(0)
  except KeyboardInterrupt:
      print("\n Critical. User aborted.")
      sys.exit(0)

if __name__=="__main__":

   sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))+'/library') #将库引入sys.path中
   main()