#! /usr/bin/env python
# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
import requests
import threading
import os
import re
import time
import platform


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
        'Accept':'*/*',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'Accept-Encoding':'gzip,deflate,br'}

key_head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
    'accept-Encoding':'gzip,deflate,br',
    'Accept':'*/*',
    'content-type': 'video/mp2t',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',    
}

def Handler(url, i, path):
    '''
    请求链接下载ts各个文件
    '''
    count = 0
    #忽略https警告
    requests.packages.urllib3.disable_warnings()
    while True:
        try:
            if count > 0:
                print("----------------------------retry----------------------------")
                print("retry url\t", url + i)
                print("retry count\t", count)
            r = requests.get(url + i, headers=headers, timeout=3, verify=False, stream=True)
            if r.status_code == 200:
                # length = len(r.content)
                # print('start download\t', 'length\t', length)
                with open(path + i.replace('/', ''), "wb") as code:
                    code.write(r.content)
                # if count > 0:
                # print("-------------------------------------------------------------")
                # print('retry download complete\t', url + i)
                # else:
                #     print('download complete\t', url + i)
                break
        except Exception as e:
            # print("----------------------------error----------------------------")
            # print(e)
            # print('error url\t', url + i)
            # count += 1
            # print('error count\t', count)
            time.sleep(1)

def getkey(url,key_path,parentPath):
    try:
        r = requests.get(url=url+key_path,headers=key_head)
        if r.status_code == 200:
            with open(parentPath+key_path,'wb') as code:
                code.write(r.content)
    except Exception as e:
        print("---------------error-----------------")
        print(e)
        time.sleep(1) 

def getM3u8File(m3u8s, base_url, resName):
    '''
    根据m3u8文件获取ts文件段,并开启线程池下载
    '''
    # 获取m3u8文件中的内容, 目前没有考虑在#里面藏url这个场景的做法。
    tss = re.findall(r'.*\n(.*\.ts)', m3u8s)
    for line in tss:
        if "#EXT-X-KEY" in line:  # 找解密Key            
            uri_pos = line.find("URI")
            key_path = line[uri_pos:len(line)].split('"')[1]
            tss.remove(line)            
    file_size = len(tss)
    # for i in tss:
    #     print(i)
    # 多线程写文件前准备工作：创建文件夹
    parentPath = os.path.dirname(os.path.dirname(__file__))
    # 获取解密的key
    path = parentPath + "/video/%s/" % resName
    # 先去下载解密的key
    getkey(base_url,key_path,path)
    if not os.path.exists(path):
        os.mkdir(path)
    # 启动多线程写文件
    print('ts files lenth:\t', file_size)
    print('start downloading,please wait mins~')
    with ThreadPoolExecutor(40) as executor:
        for each in tss:
            executor.submit(Handler, base_url, each, path)

    # 等待所有线程下载完成
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    time.sleep(1)

    print(resName, " download complete")

    
def download_file(text,context):
    '''
    用于.m3u8文件下载和可能存在的加密文件下载
    '''
    with open(text, 'a', encoding='utf-8') as result:
        for rd in context:
            result.writelines(rd)

def prepare_create(videoPath):
    '''
    python的缘故 事先创建对应文件夹
    '''
    if not os.path.exists(videoPath):
        os.mkdir(videoPath)
    
def prepare_parse(i):
    '''
        准备url的解析
    '''
    urls = re.findall(r'.*\.m3u8', i, re.S)
    url = urls[0].replace('https', 'http')
    baseUrls = re.findall(r'.*/', i, re.S)
    baseUrl = baseUrls[0].replace('https', 'http')
    names = re.findall(r'.*/(.*)\.m3u8', i, re.S)
    name = names[0]
    print("m3u8Url\t", url)
    print("baseUrl\t", baseUrl)
    print("name\t", name)
    return url,baseUrl,name

def get_m3u8_file(url,name,parentPath):
    '''
    下载.m3u8文件
    '''
    response = requests.get(url,headers=headers)
    if "#EXTM3U" not in response.text:
        raise BaseException("非M3U8的链接")
    download_file(parentPath+'/video/%s/%s.m3u8'%(name,name), response.text)
    return response.text
    
def assemble_mp4(path,parentPath,resName):
    '''
    转化成mp4
    '''
    videoPath = parentPath + '/video/%s.mp4' % resName
    sysstr = platform.system()
    if(sysstr =="Windows"):
        cmdR = r'copy /b  %s\*.ts  %s' % (os.path.abspath(path), os.path.abspath(videoPath))
        os.system(cmdR)
        time.sleep(1)
        delR = r'rmdir /s/q %s' % os.path.abspath(path)
        os.system(delR)
    else:
    #使用ffmpeg将ts合并为mp4
        # command = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s'%    (input_file,output_file)
         # command = 'ffmpeg -y -f concat -i %s -crf 18 -ar 48000 -vcodec libx264 -c:a aac -r 25 -g 25 -keyint_min 25 -strict -2 %s' % (concatfile, path)
        command  = "ffmpeg -allowed_extensions ALL -protocol_whitelist \"file,http,crypto,tcp\" "
        command += ' -y -i %s\%s.m3u8 -bsf:a aac_adtstoasc -c copy %s' % (path,resName,videoPath)
        #指行命令
        os.system(command)
        print(r"执行完成，视屏文件%s已经生成" % (videoPath))
        
if __name__ == '__main__': 
    # 准备工作：创建存放video文件夹
    parentPath = os.path.dirname(os.path.dirname(__file__))

    videoPath = parentPath + '/video/'

    print('=============================注意=============================')
    print('完整视频存放路径为:\t', videoPath)
    print('==============================================================')
    
    seeds =['']
   
    for i in seeds:
        url,baseUrl,name=prepare_parse(i)
        #创建文件夹
        prepare_create(videoPath + '/%s'%name)
        #下载.m3u8文件
        m3u8s = get_m3u8_file(url, name,parentPath)
        # 开始下载.ts文件        
        getM3u8File(m3u8s, baseUrl, name)
        # 开始拼装成mp4
        assemble_mp4(parentPath + "/video/%s/" % name,parentPath,name)

    

