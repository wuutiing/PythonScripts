# encoding: utf8

'''
author: wuting
contact: quzhouwuting@163.com
create_date: 2017-06-26
'''

import sys
from core import coroutine

@coroutine
def rank_1_handler(successor=None):
    while True:
        event = (yield)
        if event.rank == 1:
            print("+ rank_1 processed, name:{} +\n".format(event.name))
        elif successor is not None:
            successor.send(event)

@coroutine
def rank_2_handler(successor=None):
    while True:
        event = (yield)
        if event.rank == 2:
            print("++ rank_1 processed, name:{} ++\n".format(event.name))
        elif successor is not None:
            successor.send(event)

@coroutine
def rank_3_handler(successor=None):
    while True:
        event = (yield)
        if event.rank == 3:
            print("+++ rank_3 processed, name:{} +++\n".format(event.name))
        elif successor is not None:
            successor.send(event)

@coroutine
def debug_handler(successor, file=sys.stdout):
    while  True:
        event = (yield)
        file.write("*DEBUG*:{}\n".format(event))
        successor.send(event)

pipline = debug_handler(rank_3_handler(rank_2_handler(rank_1_handler())))

if __name__ == "__main__":
    pass


        
        
        
