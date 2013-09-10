# -*- coding: utf-8 -*-
import time
import options
from handlers.qhandler import Application
from db import *
import threading
import thread
from settings import *


class IS_CLOSE(threading.Thread, Application):
    def __init__(self):
        Application.__init__(self)
        threading.Thread.__init__(self)

    def run(self):
        while True:
            ts = time.time()
            for a in options.areas_time.keys():
                ct = ts - options.areas_time[a]
                if ct > 24:
                    options.areas_time.pop(a)
                    is_close_db(self.db, a)
            time.sleep(3)


def start_user_area():
    import torndb
    db = torndb.Connection(mysql_host, mysql_database, mysql_user, mysql_password)
    userarea = db.query('select * from userarea')
    import copy
    options.user_area = copy.deepcopy(userarea)
