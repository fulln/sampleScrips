#-*-coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import os
import json

url = "http://www.yanwenzi.com"

def getYwz(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,features="html.parser")
    return soup

def download_file(filename,context):
    # 准备工作：创建存放video文件夹
    parentPath = os.path.dirname(os.path.dirname(__file__))
    filename= filename.replace("/","")
    path = parentPath+'/Alfred_ywz/'+filename+'.json'
    '''
    用于JSON文件下载
    '''
    with open(path, 'a', encoding='utf-8') as result:
        json.dump(context,result,ensure_ascii=False)


def get_head_link(url):
    soup = getYwz(url) 
    down_file = {}
    nav =  soup.find(id='nav')
    for link in nav.find_all("li"):
        strs = link.a["href"]
        down_file[strs] =url+strs
    return down_file

def get_page_link(url):
    soup = getYwz(url)
    page_links = []
    page_links.append(url)
    page =  soup.find("div", class_="page")
    if page == None:
        return page_links
    for link in page.find_all("a"):
        page_links.append(url+link.attrs["href"])
    return page_links

def get_detail(url):
    soup = getYwz(url)
    informationlist = {}
    item = soup.find(id='items')
    for tr in item.find_all("li"):
        informationlist[tr.div.string] = tr.p.string
    return informationlist    

links = get_head_link(url)
# load = []
for filename in links:
    # load.append(filename.replace("/",""))
    all_pages = []
    all_context = {}
    all_pages.extend(get_page_link(links[filename]))
    for page in all_pages:
        all_context.update(get_detail(page))
    download_file(filename,all_context)


