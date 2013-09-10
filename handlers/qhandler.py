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
            (r"/editC", EditCaiHandler),
            (r"/", MainHandler),
            (r"/today", TodayHandler),
            (r"/del", DelHandler),
            (r"/tongji", TongJiHandler),
            (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, dict(path=STATIC_PATH)),
        ]
        settings = dict(
            template_path=TEMPLATE_PATH,
            static_path=STATIC_PATH,
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


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


class TodayHandler(tornado.web.RequestHandler):
    def get(self):
        j, s = back_today_json()
	self.render("today.html", day_json=s)


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
	self.redirect('/today')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        j, s = back_today_json()
        name = self.get_argument("name")
        wcai = self.get_argument("wcai")
        if wcai in j:
	    j[wcai].append(name)
	else:
	    j[wcai] = [name]

	write_today_json(j)
        self.render("index.html")


class EditCaiHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        self.set_secure_cookie("superuser", "")
        self.render("login.html")

    def post(self):
        db = self.application.db
        user = self.get_argument("user")
        password = self.get_argument("password")


class TongJiHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        #self.redirect("login")
        self.render("login.html")


def main():
    tornado.options.parse_command_line()
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
