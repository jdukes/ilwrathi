#!/usr/bin/env python
#shitty fast demo

import itertools
import json

try:
    import requests
except ImportError:
    print "pip install requests"
    raise

proxies = {'http':'http://localhost:8080'}
headers = {"Content-Type":"application/json; charset=UTF-8"}

class PetStoreClient(object):
    
    def __init__(self, baseurl):
        self.baseurl = baseurl
        self.session = requests.session()
        
    def __getattr__(self, name):
        method, endpoint = name.split('_',1)
        endpoint = '/'.join(endpoint.split('_'))
        target = self.baseurl + '/' +  endpoint
        return self.__class__.__dict__['_' + method](self, target)

    def _get(self, target):
        def _func(*args,**kwargs):
            args = '/'.join(str(a) for a in args)
            url = target + '/' + args 
            if kwargs:
                url += '?' + '&'.join("%s=%s" % i for i in kwargs.items())
            return self.session.get(url)
        return _func

    def _post(self, target):
        url = target
        def _func(jdict):
            return self.session.post(target, data=json.dumps(jdict), 
                                 headers=headers, proxies=proxies)
        return _func
    
    def _put(self, target):
        url = target
        def _func(jdict):
            return self.session.put(target, data=json.dumps(jdict), 
                                headers=headers, proxies=proxies)
        return _func
    
    def _delete(self, target):
        def _func(*args,**kwargs):
            args = '/'.join(str(a) for a in args)
            url = target + '/' + args 
            return self.session.delete(url)
        return _func