#!/usr/bin/env python
# coding=utf-8

from thing import thing

config = {
    'db': {
        'master': {
                            'url': 'mysql://root:pkuwzr@127.0.0.1:3306/massservices?charset=utf8',
                            'echo': False,
                            
        },
        'slave': {
                            'url': 'mysql://root:pkuwzr@127.0.0.1:3306/massservices?charset=utf8',
                            'echo': False,
                            
        },
                    
    },
    'redis': {
                    'host': 'localhost',
                    'port': 6379,
                    'db': 1,
                    
    },
    'thing': {
                    'debug': True,
                    
    }
            
}

thing.Thing.config(config)
