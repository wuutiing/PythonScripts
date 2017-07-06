# coding:utf-8

import os
import sys
import getopt
from datetime import datetime

from reader import XlsProxy
from module import JsonObj


def steps(input_file):
    today = datetime.strftime(datetime.today(), "%Y-%m-%d")
    output_path_prefix = os.path.join(os.getcwd(), "outputs", today)
    print(output_path_prefix)
    if not os.path.exists(output_path_prefix):
        os.mkdir(output_path_prefix)
    xp = XlsProxy(input_file)
    for sheet_name in xp:
        jo = JsonObj("module.txt")
        for k, v in xp.yield_sheet(sheet_name):
            print(k, v)
            jo.modify(v, assign_key=k, output_file_path=output_path_prefix+"/"+sheet_name)
        jo.output(file_path=output_path_prefix+"/"+sheet_name, force=True)
    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:], "h")
        opts_dic = dict(opts)
        print(args, opts_dic)
        if "-h" in opts_dic:
            print("you may input:\n    python3 steps.py <file_path>\nto generate modified json")
            return 0
        if len(args) == 1:
            return steps(args[0])
        else:
            print("not properly input parameters, just input:\n    python3 steps.py -h\nfor help.")
            return 0
    except getopt.error:
        return 0
    except Exception as e:
        print(e)
        return 2

if __name__ == "__main__":
    # steps("20170704_支付宝白户测试案例_D02.xlsx")
    sys.exit(main())