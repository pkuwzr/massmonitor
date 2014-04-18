#!/usr/bin/env python
# coding=utf-8

import web
from model import conn
from model.models.service import Service
from model.models.user import User

urls = ("/signin", "Signin",
        "/signout", "Signout",
        "/registeruser", "UserRegister",
        "/main", "Main",
        "/registerservice", "ServiceRegister",
        "/deleteservice", "ServiceRemover",
        "/showall", "ShowAll",
        "/showcustom", "ShowCustom")
app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('session'), {'login': 0})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('view') # your templates
ADMIN = ['mass@sei.pku.edu.cn', 'wangzr13@sei.pku.edu.cn']
welcom_msg = '欢迎使用'
err_msg = '用户名或者密码错误'


def logged():
    """
    A function for decide if the user has logged in.
    """
    if session.login == 1:
        return True
    else:
        return False


class ShowCustom:
    def GET(self):
        try:
            user = web.input().email
            if user in ADMIN:
                services = Service().findall()
            else:
                services = Service().findall_by_email(user)
            service_dict = {}
            for service in services:
                if service.project in service_dict:
                    service_dict[service.project].append((service.name, service.project, service.email, service.url, service.id, service.status))
                else:
                    service_dict[service.project] = [(service.name, service.project, service.email, service.url, service.id, service.status)]
            return render.show_all(service_dict)
        except Exception:
            return 'No such user!'


class ShowAll:
    """
    Show all services including their status group by their project.
    """
    def GET(self):
        if session.privilege == 1:
            services = Service().findall_by_email(session.user)
        else:
            services = Service().findall()
        service_dict = {}
        for service in services:
            if service.project in service_dict:
                service_dict[service.project].append((service.name, service.project, service.email, service.url, service.id, service.status))
            else:
                service_dict[service.project] = [(service.name, service.project, service.email, service.url, service.id, service.status)]
        return render.show_all(service_dict)


class ServiceRegister:
    def GET(self):
        # do $:f.render() in the template
        return render.register_service(1)

    def POST(self):
        data = web.input()
        query = "select * from service where name = '" + data.name + "' and project = '" + data.project + "'"
        result = Service().execute(query).rowcount
        if result == 0:
            service = Service()
            service.name = data.name
            service.project = data.project
            service.url = data.url
            service.email = session.user
            service.save()
            return render.success()
        else:
            return render.register_service(0)


class ServiceRemover:
    def POST(self):
        id = web.input().id
        Service().find(int(id)).delete()
        return '{status:ok}'


class Signin:
    def GET(self):
        if logged():
            raise web.seeother('/main')
            #return render.main()
        else:
            return render.signin(welcom_msg, 1)

    def POST(self):
        user, pwd = web.input().user, web.input().pwd
        ident = User().find_by_name(user)
        try:
            if ident and pwd == ident.pwd:
                session.user = user
                session.login = 1
                session.privilege = ident.privilege
                return render.main()
            else:
                session.login = 0
                return render.signin(err_msg, 0)
        except:
            session.login = 0
            return render.signin(err_msg, 0)


class Signout:
    def GET(self):
        session.kill()
        return render.signin(welcom_msg, 1)


class UserRegister:

    def GET(self):
        return render.register_user(welcom_msg, 1)

    def POST(self):
        user, pwd = web.input().user, web.input().pwd
        ident = User().findall_by_name(user)
        if ident:
            return render.register_user('该用户已注册', 0)
        else:
            new_user = User()
            session.user = user
            session.login = 1
            if user in ADMIN:
                session.privilege = 0
            else:
                session.privilege = 1
            new_user.name = user
            new_user.pwd = pwd
            new_user.privilege = session.privilege
            new_user.save()
            return render.main()


class Main:
     def GET(self):
         return render.main()

if __name__ == '__main__':
    app.run()
