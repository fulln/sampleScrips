#!/usr/bin/python
# encoding: utf-8

import sys
import os
import json
from workflow import Workflow3

def read_file(json_filename):
    with open(json_filename) as f:
        pop_data = json.load(f)
    return pop_data

def get_json(query):
    # parentPath = os.path.dirname(__file__)
    filename ="./"+query+".json"
    return read_file(filename)

def get_menu():
    list = ['changyong', 'gaoxing', 'maimeng', 'zhenjing', 'shengqi', 'wunai', 'yun', 'daoqian', 'dongwu', 'haixiu', 'ku', 'memeda', 'shuila', 'zaijian', 'aojiao', 'chihuo', 'deyi', 'haipa', 'jiong', 'zan', 'nanguo', 'jian', 'qita']
    list2 = ['常用', '高兴', '卖萌', '震惊', '生气', '无奈', '晕', '道歉', '动物', '害羞', '哭', '么么哒', '睡啦', '再见', '傲娇', '吃货', '得意', '害怕', '囧', '赞', '难过', '贱', '其他']
    json ={}
    for i in range(len(list)):
        json[list[i]]=list2[i]
    # for key in list:
    #     json[key] =key
    return json

def main(wf):
    args = wf.args
    arg = switch(args[0])
    if arg is None:
        flag = False
        data = get_menu()
    else:    
        flag = True
        data = get_json(arg)    
    # data = wf.cached_data(args[0],get_json(arg), max_age=600)
    for key in data:
        wf.add_item(title=data[key],subtitle=key,arg=data[key],valid=flag)        
    wf.send_feedback()

def switch(arg):
    list = ['changyong', 'gaoxing', 'maimeng', 'zhenjing', 'shengqi', 'wunai', 'yun', 'daoqian', 'dongwu', 'haixiu', 'ku', 'memeda', 'shuila', 'zaijian', 'aojiao', 'chihuo', 'deyi', 'haipa', 'jiong', 'zan', 'nanguo', 'jian', 'qita']
    if len(arg) > 1 :
        for key in list:
            if key.find(arg) != -1:
                return key
    return

if __name__ == '__main__':

    wf = Workflow3()

    sys.exit(wf.run(main))
