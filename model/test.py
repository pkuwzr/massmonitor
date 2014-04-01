#!/usr/bin/env python
# coding=utf-8

import conn
from models.service import Service

# -------- 插入数据 --------
service = Service()
service.name = 'massmonitor'
service.project = 'monitors'
service.email = 'wzr.cs09@qq.com'
service.url = 'http://localhost:8000'
service.save()

service = Service().findall()
for s in service:
    s.delete()
