#coding:utf-8
import pymongo
import requests
import time
import sys
import threading
import re
import logging
import logging.handlers

# +++++++++++++++++++++++
# config
# +++++++++++++++++++++++
def connect_to_mongo(db = 'ZLSpidersData'):
    User = "your user"
    Password = "your pwd"
    Host = "your host"
    Port = "your port"
    mongo_str = "mongodb://%s:%s@%s:%s"%(User, Password, Host, Port)
#     mongo_str = "mongodb://%s:%s"%(Host, Port)
    client = pymongo.MongoClient(mongo_str)
    sys.stdout.write("connecting to mongodb.database %s"%db)
    return client,client[db]

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

# +++++++++++++++++++++++
# config
# +++++++++++++++++++++++

class UrlManager():
    def __init__(self):
        self._urls = self.initiate_urls()
        self._dp = DataProcessor()

    def get_next_url(self):
        if self._urls == []:
            return None
        else:
            url_to_go = self._urls.pop()
            if not self._dp._db["done_urls"].find_one({"url":url_to_go}):
                self._dp._db["done_urls"].insert({"url":url_to_go})
            return url_to_go

    def initiate_urls(self):
        s = requests.Session()
        header = {'User-Agent':agent, "Accept":"application/xml"}
        origin_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/index.html"
        a = s.get(origin_url, headers = header)
        content = a.text
        url_reg = re.compile(r"<a href='(\d{2}\.html)'>")
        urls = ["http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/" + i 
            for i in url_reg.findall(content)]
        return urls

    def add_url(self, url):
        if not url in self._urls:
            try:
                if not self._dp._db["done_urls"].find_one({"url":url}):
                    self._urls.append(url)
            except:
                self._dp.repr_connetion()
                time.sleep(1)
                if not self._dp._db["done_urls"].find_one({"url":url}):
                    self._urls.append(url)

    def add_urls(self, urls):
        for url in urls:
            self.add_url(url)

    def has_urls(self):
        return True if self._urls != [] else False


class Spider():
    def __init__(self):
        self._um = UrlManager()
        self._dp = DataProcessor()
        self._logger = self.set_log() 

    def set_log(self):
        handler = logging.handlers.RotatingFileHandler("districts_spider.log", maxBytes = 1024*1024, backupCount = 5)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger = logging.getLogger('spider_logger')
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
        return logger

    def crawl(self):
        s = requests.Session()
        header = {'User-Agent':agent, "Accept":"application/xml"}
        url = self._um.get_next_url()
        try:
            a = s.get(url, headers=header)
        except:
            self._logger.warning('request failed --- ' + url)
            sys.stdout.write(url)
            return
        try:
            content = a.text.encode('windows-1252').decode('gbk')
        except:
            try:
                self._logger.warning("decode failed --- " + url)
                self.craw_urls()
            except:
                self._logger.warning("find urls failed --- " + url)
            return
        if self.craw_urls(url, content):
            self.craw_content(url, content)
        else:
            self.craw_content(url, content, flag = False)
            
    def craw_content(self, url, content, flag = True):
        domain = url[url.index('5/')+1:-5]
        if flag:
            village_reg = re.compile(r"<tr class='villagetr'>.*?<td>(\d+)</td>.*?<td>(\d+)</td>.*?<td>(.+?)<td>")
            datas = village_reg.findall(content, re.S)
            for data in datas:
                data_dic = {}
                data_dic['code'] = data[0]
                data_dic['district_type'] = data[1]
                data_dic['district_name'] = data[2]
                data_dic['domain'] = domain
                self._dp.uploade_data(data_dic)
        else:
            town_reg = re.compile(ur"<td><a href='.*?'>(\d+?)</a></td><td><a href='.*?'>([\u4e00-\u9fa5]+?)</a></td>")
            datas = town_reg.findall(content)
            for data in datas:
                data_dic = {}
                data_dic['code'] = data[0]
                data_dic['district_name'] = data[1]
                data_dic['domain'] = domain
                self._dp.uploade_data(data_dic)

    def craw_urls(self, url, content):
        url_reg = re.compile(r"<a href='(\d{2}/\d{4,9}\.html)'")
        url_part = url[:url.rindex('/')+1]
        urls = [url_part + i for i in url_reg.findall(content)]
        if urls == []:
            return "something"
        self._um.add_urls(urls)

    def craw_loop(self):
        while self._um.has_urls():
            self.crawl()
        self._dp.free_mongo()
        self._um._dp.free_mongo()


class DataProcessor:
    def __init__(self):
        self._client, self._db = connect_to_mongo()

    def uploade_data(self, data_dic):
        try:
            if self._db["districts"].find_one(data_dic):
                return
        except:
            self.repr_connetion()
            time.sleep(1)
            if self._db["districts"].find_one(data_dic):
                return
        self._db["districts"].insert(data_dic)

    def save_done(self, urls):
        for url in urls:
            try:
                if self._db["done_urls"].find_one({"url":url}):
                    continue
            except:
                self.repr_connetion()
                time.sleep(1)
                if self._db["done_urls"].find_one({"url":url}):
                    continue
            self._db.insert({"url":url})

    def fetch_done(self):
        a = self._db["done_urls"].find({}, {"_id":0,"url":1})
        done_urls = []
        for i in a:
            if not i in done_urls:
                done_urls.append(i["url"])
        return done_urls

    def repr_connetion(self):
        sys.stdout.write("repair_connection...")
        self._client.close()
        self._client, self._db = connect_to_mongo()

    def free_mongo(self):
        self._client.close()


class Monitor(threading.Thread):
    def __init__(self, spider):
        super(Monitor, self).__init__()
        self._spider = spider
        self.thread_stop = False

    def run(self):
        while True:
            sys.stdout.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" --- "+repr(len(self._spider._um._urls)))
            time.sleep(10)
            if len(self._spider._um._urls) == 0:
                time.sleep(10)
                n = 0
                sys.stdout.write("pending to exit...")
                if len(self._spider._um._urls) == 0:
                    break
        self.stop()

    def stop(self):
        self.thread_stop = True


spider = Spider()
monitor = Monitor(spider)
monitor.start()
spider.craw_loop()
sys.stdout.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" --- all finished")
