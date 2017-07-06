# coding:utf-8

from config import keyreadable_keyjson
import copy
import json
import time
from math import isnan

class JsonObj:
    '''
    封装修改操作，输出到文件操作'''
    __key = keyreadable_keyjson
    def __init__(self, path=None, jsonobj=None):
        if not (path or jsonobj):
            print("init JsonObj failed, not enough inputs")
            raise TypeError("not enough inputs to init jsonobj, path: {}, jsonobj: {}".format(path, json))
        if jsonobj:
            self._jsonobj = copy.deepcopy(jsonobj)
        elif path:
            self._jsonobj = json.load(open(path, "rb"))
        self._jsonobjs = {}
        self.counter = 0

    def modify(self, dic, assign_key=None, output_file_path="default"):
        '''
        修改，并将修改结果写入缓存'''
        def is_valid(content):
            if content:
                if type(content)==float:
                    if isnan(content):
                        return False
                return True
            else:
                return False
        self._jsonobj_copy = copy.deepcopy(self._jsonobj)
        for k in dic:
            json_path = self.__key.get(k, None)
            if json_path is None:
                raise KeyError("key {} not configed".format(k))
            if is_valid(dic[k]):
                self._set_value(json_path, dic[k])
        if assign_key is None:
            self._jsonobjs[time.time()] = self._jsonobj
        else:
            self._jsonobjs[str(assign_key)] = self._jsonobj
        self._jsonobj = self._jsonobj_copy
        self.output(output_file_path)

    def _set_value(self, json_path, value):
        '''
        修改值'''
        tmp_path = "".join(["['{}']".format(i) for i in json_path.split(".")])
        exec("self._jsonobj{} = value".format(tmp_path))

    def output(self, file_path="template", force=False):
        if len(self._jsonobjs)>1000 or force:
            file_path += "_"+str(self.counter)+".txt"
            with open(file_path, "w") as f:
                json.dump(self._jsonobjs, f)
            self._jsonobjs = {}
            self.counter += 1



if __name__ == "__main__":
    # a = json.load(open("module.txt", "rb"))
    # j = JsonObj(a)
    # # REJECT  3   TRUE    A016    3
    # j.modify({"decision": "REJECT", "field": 3, "is_targeted": True, "rule_info": "A016", "target_lev": 3})
    # j.output("jjjjjj", force=True)
    pass
