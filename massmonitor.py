#!/usr/bin/env python
# coding=utf-8

import web
from model import conn
from model.models.service import Service

urls = ("/signin", "Signin",
        "/registeruser", "UserRegister",
        "/main", "Main",
        "/registerservice", "ServiceRegister",
       "/showall", "ShowAll")
app = web.application(urls, globals())

render = web.template.render('view') # your templates


class ShowAll:
    """
    Show all services including their status group by their project.
    """
    def GET(self):
        services = Service().findall()
        service_dict = {}
        for service in services:
            if service.project in service_dict:
                service_dict[service.project].append(service)
            else:
                service_dict[service.project] = []
                service_dict[service.project].append(service)
        print service_dict.keys()
        return render.show_all(service_dict)


class ServiceRegister:
    def GET(self):
        # do $:f.render() in the template
        return render.register_service()

    def POST(self):
        data = web.input()
        print data.keys()
        service = Service()
        service.name = data.name
        service.project = data.project
        service.url = data.url
        service.email = data.email
        service.save()
        return render.success()


class Signin:
     def GET(self):
         return render.signin()


class UserRegister:
     def GET(self):
         return render.register_user()


class Main:
     def GET(self):
         return render.main()

if __name__ == '__main__':
    app.run()
