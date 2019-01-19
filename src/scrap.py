
import urllib.request
import numpy as np
import random
import re
import os
import time
import bs4 as bs
import pandas as pd
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

HEADERS = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}
DB_FILE = 'etherscamdb.json'
DB = json.load(open(DB_FILE,'r'))
print(len(DB.keys()))


keys = list(DB.keys())

def getSinglePageHackList(page_no=1):  
    # print(page_no)
    hackUrl ='https://etherscan.io/accounts/'+str(page_no)+'?l=Phish%2fHack'
    req=urllib.request.Request(hackUrl, headers=HEADERS)
    html_source = urllib.request.urlopen(req).read()
    html_name = 'scrap/hackList'+'-'+str(page_no)+'.html'
    f = open(html_name,'wb')
    f.write(html_source)
    f.close()
    soup = bs.BeautifulSoup(html_source, 'html')
    body = soup.find('tbody')
    trs = body.find_all('tr')

    # print(len(trs)) 
    hack_list= []

    for tr in trs: 
        tds = tr.find_all('td')
        addr = tds[1].text
        label = tds[2].text
        bal = float(tds[3].text.split(' ')[0].replace(',',''))
        txn = int(tds[4].text)
        print(addr, label, bal, txn)

        item = {
            'address':addr,
            "label":label,
            'balance':bal,
            'transactions':txn
        }
        if txn >= 10:
            hack_list.append(item)

    return hack_list
                

def getHackList():
    all_list = []
    for page_no in range(0,9):
        scam_list = getSinglePageHackList(page_no)
        all_list+=scam_list
    print(len(all_list))

    json.dump(all_list, open('hackList.json','w'), indent=4)


def getAddressComments(addr, folder = 'hackComments/'):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("https://etherscan.io/address/"+str(addr))
    button = driver.find_element_by_id("ContentPlaceHolder1_li_disqus")
    button.click()

    t=3+random.random()*3
    print(t)
    time.sleep(t)
    url = driver.find_element_by_id('disqus_thread').find_element_by_tag_name('iframe').get_attribute('src')
    # url = 'https://etherscan.disqus.com/'+str(key)+'/latest.rss'
    driver.close()

    print(url)

    req=urllib.request.Request(url, headers=HEADERS)
    html_source = urllib.request.urlopen(req).read().decode("UTF-8")
    html_name = folder+str(addr)+'.html'
    f = open(html_name,'w')
    f.write(html_source)
    f.close()

    soup = bs.BeautifulSoup(html_source,'html')
    script = soup.find('script',{'id':'disqus-threadData'})
    obj = json.loads(script.text)
    posts = obj['response']['posts']
    # print(posts)
    raw_comments = [post['raw_message'] for post in posts]
    result = {
        "address":addr,
        "commentsLink":url,
        "comments": ' || '.join(raw_comments[0:10]).replace(',',' ').replace('\n',' '),
        "commentsCount": len(raw_comments)
        # "commentsDetails":posts
    }
    # print(result)
    return  result

 

def getHackComments():
    hack_list = json.load(open('hackList.json','r'))
    i=0
    hack_list_with_comments = []
    for item in hack_list:
        i+=1
        print(i)
        addr = item['address']
        comments = getAddressComments(addr, 'hackComments/')
        item['commentsLink'] = comments['commentsLink']
        item['comments'] = comments['comments']
        item['commentsCount'] = comments['commentsCount']
        hack_list_with_comments.append(item)
    json.dump(hack_list_with_comments,open('hack_list_withcomments.json','w'), indent=4)
    

def getGoodComments():
    good_list = json.load(open('goodList.json','r'))
    i=0
    good_list_with_comments = []
    for item in good_list:
        i+=1
        print(i)
        addr = item['exchange']
        comments = getAddressComments(addr, 'goodComments/')
        item['commentsLink'] = comments['commentsLink']
        item['comments'] = comments['comments']
        item['commentsCount'] = comments['commentsCount']
        item['address'] = addr
        del item['exchange']
        good_list_with_comments.append(item)
    json.dump(good_list_with_comments,open('good_list_withcomments.json','w'), indent=4)
    # print(resul

getGoodComments()
# getComments()







# for key in keys[0:10]:
#     driver = webdriver.Chrome('chromedriver.exe')
#     driver.get("https://etherscan.io/address/"+str(key))
#     button = driver.find_element_by_id("ContentPlaceHolder1_li_disqus")
#     button.click()
#     time.sleep(3)
#     url = driver.find_element_by_id('disqus_thread').find_element_by_tag_name('iframe').get_attribute('src')
#     # url = 'https://etherscan.disqus.com/'+str(key)+'/latest.rss'
#     driver.close()
    
#     print(url)
#     req=urllib.request.Request(url, headers=HEADERS)
#     html_source = urllib.request.urlopen(req).read().decode("UTF-8")
#     html_name = 'htmls/'+str(key)+'.html'
#     f = open(html_name,'w')
#     f.write(html_source)
#     f.close()

    #     for desc in soup.find_all('channel'):
#         text = desc.text.replace('<p>','').replace('</p>','').replace('<br>','').replace('<a>','').replace('</a>','')
#         print(text)
    
#     for item in soup.find_all('item'):
#         desc = item.find('description')
#         print(desc.text)
#         ps =soup.find_all('p')
#         print(ps)
# #         print(ps)
#         for p in ps:
#             print(p.get_text())
        
    

#     print(item)
    # soup = bs.BeautifulSoup(item,'lxml')
    # print(soup)