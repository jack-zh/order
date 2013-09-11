#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.options import define, options
import json
import os.path
import time
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from log import logger
import settings as allset

define("port", default=allset.host_port, help="run port", type=int)

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "../static")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/today", TodayHandler),
            (r"/del", DelHandler),
            (r"/tongji", TongJiHandler),
            
            (r"/addc", AddCaiHandler),
            (r"/delc", DelCaiHandler),
            (r"/listc", ListCaiHandler),
	    
	    (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, dict(path=STATIC_PATH)),
        ]
        settings = dict(
            template_path=TEMPLATE_PATH,
            static_path=STATIC_PATH,
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)



class TodayHandler(tornado.web.RequestHandler):
    def get(self):
	self.redirect('/')


class DelHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("del.html")

    def post(self):
        name = self.get_argument("name")
	j, s = back_today_json()
	for c in j:
	    if name in j[c]:
	        j[c].remove(name)
		if len(j[c]) == 0:
		    j.pop(c)
		    break
	write_today_json(j)
	self.redirect('/')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
	c_list, c_str = back_cai_list()
	t_list, t_str = back_today_json()
        self.render("index.html", c_str=c_str, t_str=t_str)

    def post(self):
        j, s = back_today_json()
        name = self.get_argument("name")
        wcai = self.get_argument("wcai")
        if wcai in j:
	    j[wcai].append(name)
	else:
	    j[wcai] = [name]

	write_today_json(j)
	c_list, c_str = back_cai_list()
	t_list, t_str = back_today_json()
        self.render("index.html", c_str=c_str, t_str=t_str)


class AddCaiHandler(tornado.web.RequestHandler):
    def post(self):
	c_list, c_str = back_cai_list()
        name = self.get_argument("name")
        price = self.get_argument("price")
	c_list[name] = price
	write_cai_list(c_list)
	self.redirect('/listc')


class DelCaiHandler(tornado.web.RequestHandler):
    def post(self):
	c_list, c_str = back_cai_list()
        name = self.get_argument("name")
	if name in c_list:
	    del(c_list[name])
	    write_cai_list(c_list)
	self.redirect('/listc')


class ListCaiHandler(tornado.web.RequestHandler):
    def get(self):
	c_list, c_str = back_cai_list()
        self.render("listc.html", c_list=c_list, c_str=c_str)


class TongJiHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        #self.redirect("login")
        self.render("login.html")


def back_cai_list():
	c_json = {} 
	c_str = ""
	file_name = allset.data_dir + "clist.json"
	if os.path.exists(file_name):
	    fd = open(file_name, "r")
	    c_str = fd.read()
	    fd.close()
	    c_json = json.loads(c_str, encoding="utf-8")
	return (c_json, c_str)


def write_cai_list(j):
	file_name = allset.data_dir + "clist.json"
	fd = open(file_name, "wt")
	fd.write(json.dumps(j, indent=1, ensure_ascii=False))
	fd.close()


def back_today_json():
	day_json = {} 
	json_str = ""
	date_str = time.strftime('%Y-%m-%d', time.localtime(int(time.time())))
	file_name = allset.data_dir + date_str
	if os.path.exists(file_name):
	    fd = open(file_name, "r")
	    json_str = fd.read()
	    fd.close()
	    day_json = json.loads(json_str, encoding="utf-8")
	return (day_json, json_str)


def write_today_json(j):
	date_str = time.strftime('%Y-%m-%d', time.localtime(int(time.time())))
	file_name = allset.data_dir + date_str
	fd = open(file_name, "wt")
	fd.write(json.dumps(j, indent=1, ensure_ascii=False))
	fd.close()


def main():
    tornado.options.parse_command_line()
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
