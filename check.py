#!/usr/bin/env python
# coding=utf-8

from model import conn
from model.models.service import Service

def check(url):
    """check the url status"""
    import requests
    try:
        r = requests.get(url, timeout=0.1)
        if r.status_code == requests.codes.ok:
            return 'available'
        else:
            return 'unavailable'
    except requests.exceptions.RequestException:
        return 'unavailable'


services = Service().findall()
for service in services:
    service.status = check(service.url)
    service.save()
