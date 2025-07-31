import json

def load_json(path):
    with open(path,'r',encoding='utf-8') as f:
        load = json.load(f)
        return load
        
def dumps_json(path,obj):
    with open(path,'w',encoding='utf-8') as f:
        write = json.dumps(obj,f)
        return write

def read_txt(path):
    with open(path,'r',encoding='utf-8') as f:
        read = f.read()
        return read

def readlines_txt(path):
    with open(path,'r',encoding='utf-8') as f:
        read = [line.strip() for line in f.readlines()]
        return read

def write_txt(path,text:str):
    with open(path,'w',encoding='utf-8') as f:
        write = f.write(text)
        return write

def writelines_txt(path):
    with open(path,'w',encoding='utf-8') as f:
        write = f.writelines(text)
        return write


        
        
        