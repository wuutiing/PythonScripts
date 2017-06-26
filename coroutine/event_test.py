# encoding: utf8

'''
author: wuting
contact: quzhouwuting@163.com
create_date: 2017-06-26
'''
import time
import random
import threading
from core import Ensurer, ensure_preoperty, not_null, str_only, int_only

@ensure_preoperty
class Event:
    name = Ensurer([not_null, str_only])
    desc = Ensurer(str_only)
    rank = Ensurer(int_only)
    event_type = Ensurer(str_only)
    def __init__(self, name, detail={}):
        self.name = name
        self.desc = detail.get("detail")
        self.rank = detail.get("rank")
        self.event_type = detail.get("event_type")

    def __str__(self):
        basic = "<Event@{}>[name]:{}".format(id(self), self.name)
        for name, attr in self.__dict__.items():
            name = name[2:]
            if name in ["desc", "rank", "event_type"]:
                if attr is not None:
                    basic += ",[{}]:{}".format(name, attr)
        return basic


@ensure_preoperty
class EventCollection():
    name = Ensurer([not_null, str_only])
    time_esc = Ensurer(int_only)
    def __init__(self, name, time_esc, rank_range=3):
        self.rank_range = (1, rank_range)
        self.events = []
        self.name = name
        self.time_esc = time_esc

    def next(self):
        while True:
            if self.events:
                return self.events.pop()
            else:
                time.sleep(self.time_esc+1)

    def add(self, event):
        self.events.append(event)

    def event_start(self):
        names = ["A", "B", "C"]
        def add_many():
            while True:
                rank = {"rank": random.randint(*self.rank_range)}
                event = Event(random.choice(names), detail=rank)
                self.events.append(event)
                time.sleep(1)
                if len(self.events)>10:
                    break
        threading.Thread(target=add_many, name="add_many").start()

if __name__ == "__main__":
    pass


        
        
        
