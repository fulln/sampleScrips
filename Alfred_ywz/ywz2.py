#-*-coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import os
import json

url = "http://www.hehuan.co"

def getYwz(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,features="html.parser")
    return soup

def download_file(filename,context):
    # 准备工作：创建存放video文件夹
    parentPath = os.path.dirname(os.path.dirname(__file__))
    filename= filename.replace("/tag/","")
    tmp_name=''
    for i in filename:
        if i == '-':
            break
        tmp_name = tmp_name+i
    filename = tmp_name
    path = parentPath+'/Alfred_ywz/'+filename+'.json'
    '''
    用于JSON文件下载
    '''
    if not os.path.exists(path):
        os.system(r"touch {}".format(path))#调用系统命令行来创建文件
    with open(path, 'w', encoding='utf-8') as result:
        json.dump(context,result,ensure_ascii=False)


def get_tag_link(urls):
    soup = getYwz(urls) 
    down_file = {}
    menu_list = soup.find(class_ = 'menu-list')
    # nav =  soup.find(id='nav')
    for link in menu_list.find_all("li"):
        strs = link.a["href"]
        down_file[strs] =url+strs
    return down_file

def get_page_link(urls):
    soup = getYwz(urls)
    page_links = []
    page_links.append(urls)
    page =  soup.find("ul", class_="pagelist")
    if page == None:
        return page_links
    for link in page.find_all("a"):
        page_links.append(url+link.attrs["href"])
    return page_links

def get_detail(url):
    soup = getYwz(url)
    informationlist = {}
    item = soup.find(class_='article-list')
    for tr in item.find_all(class_='face-item'):
        face = tr.find(class_='face').string
        name = tr.a['title']
        informationlist[name] = face
    return informationlist    


links = get_tag_link(url)
for filename in links:
    all_pages = []
    all_context = {}
    all_pages.extend(get_page_link(links[filename]))
    for page in all_pages:
        print(page)
        all_context.update(get_detail(page))
    download_file(filename,all_context)


