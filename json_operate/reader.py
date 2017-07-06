# coding:utf-8

import pandas as pd
import xlrd
import numpy as np

from module import JsonObj

class XlsProxy:
    '''
    读取xls文件（暂存）'''
    def __init__(self, path):
        self._path = path
        self._workbook = None
        self._dfs = {}

    def __iter__(self):
        if self._workbook is None:
            self._workbook = xlrd.open_workbook(self._path)
        for sheet in self._workbook.sheets():
            yield sheet.name

    def get_sheet_content(self, sheet_name):
        if not sheet_name in self._dfs:
            try:
                self._dfs[sheet_name] = pd.read_excel(self._path, sheetname=sheet_name).set_index("案例编号")
            except Exception as e:
                print("something wrong during open excel {}, sheet {}".format(self._path, sheet_name))
                raise RuntimeError("something wrong during open excel {}, sheet {}".format(self._path, sheet_name))
        return self._dfs[sheet_name].to_dict("index")

    def yield_sheet(self, sheet_name):
        dicts = self.get_sheet_content(sheet_name)
        for k in dicts:
            yield k, dicts[k]

        


# xp = XlsProxy("20170704_支付宝白户测试案例_D02.xlsx")
# jo = JsonObj(path="module.txt")

# for i in xp:
#     print(i, ...)

# for j,k in xp.yield_sheet("通用1"):
#     print(j,k, ...)
#     jo.modify(k, j, "通用1")
# jo.output("通用1", force=True)


