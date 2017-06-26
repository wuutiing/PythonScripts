# encoding: utf8

'''
author: wuting
contact: quzhouwuting@163.com
create_date: 2017-06-26
'''

from coroutine import pipline
from event_test import EventCollection

if __name__ == "__main__":
    ec = EventCollection(name="ec", time_esc=1)
    ec.event_start()
    while True:
        event = ec.next()
        pipline.send(event)

