#!/usr/bin/env python
# coding=utf-8

import conn
from models.service import Service

services = Service().findall()
for service in services:
    service.status = 'available'
    service.save()
