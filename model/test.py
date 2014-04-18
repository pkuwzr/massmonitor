#!/usr/bin/env python
# coding=utf-8

import conn
from models.service import Service

s = Service().find(5)
print s.id
