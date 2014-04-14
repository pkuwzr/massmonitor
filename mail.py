#!/usr/bin/env python
# coding=utf-8

import web
from model import conn
from model.models.user import User
from model.models.service import Service

#settings for email
web.config.smtp_server = 'mail.sei.pku.edu.cn'
web.config.smtp_port = 25
web.config.smtp_username = 'wangzr13'
web.config.smtp_password = 'pkuwzr13'
#web.config.smtp_starttls = True

FROM = 'wangzr13@sei.pku.edu.cn'
TO = ''
SUBJECT = 'Monitor information for services'
TEMPLATE = u'<html><body><p>您注册的服务状态：</p><table border="1"><tr><th>工程</th><th>服务总数</th><th>不可访问服务数</th></tr>%s</table><p>更多细节请查看<a href="%s"> 链接 </a>。</p></body></html>'
MESSAGE = ''
LINK_BASE = 'http://localhost:8080/showcustom?email=%s'
LINK = ''

users = User().findall()
for user in users:
    data = ''
    TO = user.name
    LINK = LINK_BASE % TO
    services = Service().findall_by_email(TO)
    service_dict = {}
    line = '<tr><td>%s</td><td>%s</td><td>%s</td></tr>'
    for service in services:
        if service.project not in service_dict:
            service_dict[service.project] = [0, 0]
        service_dict[service.project][0] += 1
        if service.status == 'unavailable':
            service_dict[service.project][1] += 1
    for k, v in service_dict.items():
        data += (line % (k, v[0], v[1]))
    MESSAGE = TEMPLATE % (data, LINK)
    web.sendmail(FROM, TO, SUBJECT, MESSAGE, headers={'content-type':'text/html;charset=utf-8'})
