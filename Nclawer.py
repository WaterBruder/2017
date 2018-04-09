from selenium import webdriver
import re
import pandas as pd
from time import sleep
import numpy as np
import threading

# y=0

# for i in data['正题名']:
#  i=re.sub(r"\d*月\d*日|\([0-9]+\)","",i)
#  data['正题名'][y]=i
#  y=y+1

li = ['电视剧场\\大陆剧场', '电视剧场\\港台剧场', '电视剧场', '电视剧场\\日韩剧场', '电视剧场\\欧美剧场', '家庭影院\\其他', '家庭影院\\动作', '家庭影院\\爱情', '电视剧场/大陆剧场',
      '家庭影院\\喜剧', '家庭影院\\恐怖', '电视剧场\\其他', '电视剧场 电视剧场\\大陆剧场', '家庭影院\\悬念', '家庭影院\\科幻', '家庭影院\\动画片', '电视剧场\\其他剧场', '家庭影院',
      '家庭影院/动作', '家庭影院\\警匪', '家庭影院\\战争', '家庭影院\\文艺', '家庭影院\\动作片', '电视剧场/欧美剧场', '家庭影院\\犯罪', '家庭影院\\历史', '教学教育\\纪录片',
      '家庭影院/灾难']
#lis = ['广告', '科学教育\\纪录片', '体育竞技', '生活服务', '科学教育', '新闻时事', '综艺娱乐']


def firefoxclawer(x):
    if data['分类名称'].ix[x] in li:
        sc = data['正题名'].ix[x]
        options = webdriver.FirefoxOptions()
        options.set_headless()
        options.add_argument('--disable-gpu')
        driver = webdriver.Firefox(firefox_options=options)
        driver.get('https://movie.douban.com/subject_search?search_text=%s&cat=1002' % sc)
        #sleep(1.5)
        try:
            driver.find_element_by_css_selector("a.cover-link").click()
            #sleep(1.5)
            driver.find_elements_by_xpath("//span[@property='v:genre']")
            str = ''
            for i in driver.find_elements_by_xpath("//span[@property='v:genre']"):
                str = str + '.'+i.text
            newcln[x] = str
            driver.close()
        except:
            driver.close()
            print('缺%d'%x)
            data['类型']=newcln
            data.to_excel(r'C:\Users\xujianmiao\Desktop\test1\%d.xls'%x)
    else:
        newcln[x] = data['分类名称'].ix[x]

def ieclawer(x):
    if data['分类名称'].ix[x] in li:
        sc = data['正题名'].ix[x]
        driver = webdriver.Ie()
        driver.get('https://movie.douban.com/subject_search?search_text=%s&cat=1002' % sc)
        #sleep(1.5)
        try:
            driver.find_element_by_css_selector("a.cover-link").click()
            #sleep(1.5)
            driver.find_elements_by_xpath("//span[@property='v:genre']")
            str = ''
            for i in driver.find_elements_by_xpath("//span[@property='v:genre']"):
                str = str + '.'+i.text
            newcln[x] = str
            driver.close()
        except:
            driver.close()
            print('缺%d'%x)
            data['类型']=newcln
            data.to_excel(r'C:\Users\xujianmiao\Desktop\test1\%d.xls'%x)
    else:
        newcln[x] = data['分类名称'].ix[x]

def chromeclawer(x):
    if data['分类名称'].ix[x] in li:
        sc = data['正题名'].ix[x]
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--disable-infobars')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://movie.douban.com/subject_search?search_text=%s&cat=1002' % sc)
        #sleep(1.5)
        try:
            driver.find_element_by_css_selector("a.cover-link").click()
            #sleep(1.5)
            driver.find_elements_by_xpath("//span[@property='v:genre']")
            str = ''
            for i in driver.find_elements_by_xpath("//span[@property='v:genre']"):
                str = str + '.'+i.text
            newcln[x] = str
            driver.close()
        except:
            driver.close()
            print('缺%d'%x)
            data['类型']=newcln
            data.to_excel(r'C:\Users\xujianmiao\Desktop\test1\%d.xls'%x)
    else:
        newcln[x] = data['分类名称'].ix[x]

if __name__ == "__main__":

    global data
    global newcln
    lip = []
    threads = []
    filepath = r'C:\Users\xujianmiao\Desktop\test1\1050.xls'
    data = pd.read_excel(filepath)
    #newcln = pd.Series(np.zeros(data.shape[0]))
    #newcln.astype(str)
    if '类型'  in data.columns:
     newcln=data['类型']
     no=re.compile(r'(\d+)\.xls').findall(filepath)[0]
     no=int(no)
     for p in range(no):
        lip.append(p)
    else:
      newcln = pd.Series(np.zeros(data.shape[0]))
      newcln.astype(str)
      data.insert(1, '类型', newcln)
      for p in range(data.shape[0]):
          lip.append(p)
    lis=[firefoxclawer,chromeclawer]
    print (p)
    thread = threading.Thread(target=lis.pop()(lip.pop()))
    thread.setDaemon(True)  # set daemon so main thread can exit when receives ctrl-c
    thread.start()
    threads.append(thread)
    try:
        while threads or lip:
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
                while len(threads) < 5 and lip and lis :
                    x=lip.pop()
                    thread = threading.Thread(target=lis.pop()(x))
                    thread.setDaemon(True)  # set daemon so main thread can exit when receives ctrl-c
                    thread.start()
                    print(x)
                    threads.append(thread)
                    if x%10==0:
                        data['类型'] = newcln
                        data.to_excel(r'C:\Users\xujianmiao\Desktop\test1\%d.xls' % x)
                # all threads have been processed
                # sleep temporarily so CPU can focus execution on other threads
                sleep(1)
    except KeyboardInterrupt:
        data.insert(1, '类型', newcln)
        data.to_excel(r'C:\Users\xujianmiao\Desktop\2.xls')
    if lip:
        print(x)
    else:
        data['类型'] = newcln
        data.to_excel(r'C:\Users\xujianmiao\Desktop\T.xls')