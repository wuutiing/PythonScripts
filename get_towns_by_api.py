#coding:utf-8
import pymongo
import requests
import json
import time
import threading
import re
import logging
import logging.handlers
from datetime import datetime

# ++++++++++++++++++++++++
# config
# ++++++++++++++++++++++++

def connect_to_mongo_home(db = 'testdb'):
    User = "user"
    Password = "pwd"
    Host = "your host"
    Port = "port"
    mongo_str = "mongodb://%s:%s@%s:%s"%(User, Password, Host, Port)
    # mongo_str = "mongodb://%s:%s"%(Host, Port)
    client = pymongo.MongoClient(mongo_str)
    print "connecting to mongodbhome.database %s"%db
    return client,client[db]

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

api_url="http://route.showapi.com/1149-2"

api_sec = "2db5a033976f47e1a745ae7740a2463a"

app_id = "33986"

# ++++++++++++++++++++++++
# config
# ++++++++++++++++++++++++

class LoggerEnabledObj():
    def __init__(self, logfile):
        self._logger = self.set_log(logfile)

    def set_log(self, logfile):
        handler = logging.handlers.RotatingFileHandler(logfile, maxBytes = 1024*1024, backupCount = 5)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger = logging.getLogger('spider_logger')
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
        return logger


class MongoManager(LoggerEnabledObj):
    def __init__(self):
        super(MongoManager, self).__init__("get_towns_by_api.log")
        self._client, self._db = connect_to_mongo_home()

    def free_mongo(self):
        self._client.close()

    def repr_mongo(self, fun):
        self._logger.warning("method restart mongo: " + fun)
        self._client.close()
        self._client, self._db = connect_to_mongo_home()
        time.sleep(1)

    def has_unhandled(self):
        return self._db["city_tree"].find_one({"searchTime":{"$exists":False}})

    def pop_a_zipcode(self):
        try:
            p = self._db["city_tree"].find_one({"searchTime":{"$exists":False}})
        except:
            self.repr_mongo("pop_a_zipcode")
            p = self._db["city_tree"].find_one({"searchTime":{"$exists":False}})
        if p is not None:
            return p["id"]
        return p

    def update_parent(self, _id, new_data):
        try:
            self._db["city_tree"].update({"id":_id}, {"$set":new_data}, multi = False)
        except:
            self.repr_mongo("update_parent")
            self._db["city_tree"].update({"id":_id}, {"$set":new_data}, multi = False)

    def handle_datas(self, parent_id, son_dict):
        def remove_dup(a_list):
        '''sometimes there will be duplicated data returned back,
        this method deals with that.
        '''
            length = len(a_list)
            dup_list = []
            for i in xrange(length):
                for j in xrange(i+1, length):
                    if a_list[i]["id"] == a_list[j]["id"]:
                        dup_list.append(a_list[i])
                        break
            for i in dup_list:
                a_list.remove(i)

        if son_dict["showapi_res_body"]["ret_code"] == "-1":
            self.insert_sons(parent_id, [])
        else:
            remove_dup(son_dict["showapi_res_body"]["data"])
            self.insert_sons(parent_id, son_dict["showapi_res_body"]["data"])

    def insert_sons(self, parent_id, son_list):
        if son_list == []:
            self.update_parent(parent_id, {"searchTime":datetime.now()})
            return
        try:
            self._db["city_tree"].insert_many(son_list)
        except:
            self.repr_mongo("insert_sons")
            self._db["city_tree"].insert_many(son_list)
        self.update_parent(parent_id, {"searchTime":datetime.now()})


class ApiRequest():
    def __init__(self):
        self._mm = MongoManager()
        self._s = requests.Session()

    def request_api(self, _id):
        final_api_url = api_url + "?showapi_appid=%s&showapi_sign=%s&parentId=%s"%(app_id, api_sec, _id)
        a = self._s.get(final_api_url)
        return json.loads(a.text)

    def req_loop(self):
        while self._mm.has_unhandled():
            _id = self._mm.pop_a_zipcode()
            datas = self.request_api(_id)
            self._mm.handle_datas(_id, datas)
        self._mm.free_mongo()


if __name__ == "__main__":
    ar = ApiRequest()
    ar.req_loop()
