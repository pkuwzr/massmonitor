#!/usr/bin/env python
# coding=utf-8

import conn
from models.service import Service
from models.user import User

#services = Service().findall_by_email('wzr.cs09@qq.com')
services = Service().findall()
service_dict = {}
for service in services:
    tmp = service
    if tmp.project in service_dict:
        service_dict[tmp.project].append(tmp)
    else:
        service_dict[tmp.project] = [tmp]

print service_dict
