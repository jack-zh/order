from json.encoder import JSONEncoder
import json
import tornado.web
import options


class SuperBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("superuser")


class SuperIndexHandler(SuperBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("super/userManagement.html")

    @tornado.web.authenticated
    def post(self):
        self.write("SuperIndexHandler post")


class SuperUserInfoHandler(SuperBaseHandler):
    @tornado.web.authenticated
    def get(self):
        db = self.application.db
        users = db.query("select * from user where authorization=0")
        self.write(json.dumps(users))

    @tornado.web.authenticated
    def post(self):
        db = self.application.db
        action = self.get_arguments('action')[0]
        if action == 'addUser':
            data = self.get_arguments('data')[0]
            name = data.split(':::;;;')[0]
            password = data.split(':::;;;')[1]
            try:
                sql = 'INSERT INTO user(username, passwd) VALUES '+'("'+name+'","'+password+'")'
                db.execute(sql)
                self.write('Success')
            except:
                self.write('Failure')
        elif action == 'deleteUser':
            user = self.get_arguments('user')[0]
            sql = 'delete from userarea where username="'+user+'"'
            db.execute(sql)
            sql = 'delete from user where username="'+user+'"'
            db.execute(sql)
            self.write('Success')
        elif action == 'modifyUser':
            user = self.get_arguments('user')[0]
            password = self.get_arguments('newpassword')[0]
            sql = 'update user set passwd="'+password+'" where username="'+user+'"'
            db.execute(sql)
            self.write('Success')


class SuperAreaInfoHandler(SuperBaseHandler):
    @tornado.web.authenticated
    def get(self):
        db = self.application.db
        areas = db.query("select * from area")
        self.write(json.dumps(areas))


class SuperUserAreaInfoHandler(SuperBaseHandler):
    @tornado.web.authenticated
    def get(self):
        db = self.application.db
        user = self.get_arguments('user')[0]
        if not user or user == 'all':
            userareas = db.query("select * from userarea ")
        else:
            userareas = db.query("select * from userarea where username='"+user+"'")
        self.write(json.dumps(userareas))

    @tornado.web.authenticated
    def post(self):
        db = self.application.db
        data = self.get_arguments('data')[0]
        l = data.split(':::;;;')
        user = self.get_arguments('user')[0]
        insertsql = 'INSERT INTO userarea(username, areanum) VALUES '
        for area in l:
            insertsql = insertsql+'("'+user+'",'+area+'),'
        sql = 'delete from userarea where username="'+user+'"'
        db.execute(sql)
        if area:
            db.execute(insertsql[:-1])
        
	userarea = db.query('select * from userarea')
        import copy
        options.user_area = copy.deepcopy(userarea)
        self.write('Success')
