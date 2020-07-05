import os
import json

path = os.path.dirname(__file__)
cachefile = {}

def read_file(json_filename):
    with open(json_filename) as f:
        pop_data = json.load(f)
    return pop_data

def write_file(filename,context):
    # 准备工作：创建存放json文件夹
    parentPath = os.path.dirname(os.path.dirname(__file__))
    filename= filename.replace("/tag/","")
    tmp_name=''
    for i in filename:
        if i == '-':
            break
        tmp_name = tmp_name+i
    filename = tmp_name
    path = parentPath+'/Alfred_ywz/'+filename
    '''
    用于JSON文件下载
    '''
    if not os.path.exists(path):
        os.system(r"touch {}".format(path))#调用系统命令行来创建文件
    with open(path, 'w', encoding='utf-8') as result:
        json.dump(context,result,ensure_ascii=False)


def get_json(query):
    # parentPath = os.path.dirname(__file__)
    return read_file(query)

dirname=[]

for dirpath,dirnames,filenames in os.walk(path+"/a/"):
    for filename in filenames:
        dirname.append(filename.replace(".json",""))    
    #     if filename.endswith(".json") :
    #         if ord(filename[:1]) < 65:
    #             continue
    #         smalljson =  get_json(dirpath+'/'+filename)
    #         for key,value in smalljson.items():    
    #                 cachefile.update(get_json(dirpath+'/'+filename))
    # write_file("all.json",cachefile)        
            
print(dirname)
