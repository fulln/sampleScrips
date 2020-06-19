#!/usr/bin/python
# encoding: utf-8

import sys
import json

def read_file(json_filename):
    with open(json_filename) as f:
        pop_data = json.load(f)
    return pop_data

def get_json(query):
    # parentPath = os.path.dirname(__file__)
    filename ="./"+query+".json"
    return read_file(filename)

def switch(arg):
    list = ['changyong', 'gaoxing', 'maimeng', 'zhenjing', 'shengqi', 'wunai', 'yun', 'daoqian', 'dongwu', 'haixiu', 'ku', 'memeda', 'shuila', 'zaijian', 'aojiao', 'chihuo', 'deyi', 'haipa', 'jiong', 'zan', 'nanguo', 'jian', 'qita']
    if len(arg) > 2 :
        for key in list:
            if key.find(arg) != -1:
                return key
    return 

def get_xml(query):
    arg = switch(query)
    if arg is None:
        return
    data = get_json(arg)
    strs = """<item arg="{0}">
            <title>{0}</title>
            <subtitle>{1}</subtitle>
            <icon>icon.png</icon>
            </item>
        """
    out = []
    for key in data:
        out.append(strs.format(data[key],key))
    print(''.join(out))
