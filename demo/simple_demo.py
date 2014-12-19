#!/usr/bin/env python
from __future__ import print_function
from ilwrathi import IdempotentAccessor

class MyIdempotentAccessor(IdempotentAccessor):
    
    def get_spam(self):
        print("execing spam")
        return "spam"
    
    def get_eggs(self):
        print("execing eggs")
        return "eggs"

    def get_spamandeggs(self):
        print("execing spamandeggs")
        return "spam and eggs relies on %(spam)s and %(eggs)s" % self

#myIdempotentAccessor = MyIdempotentAccessor("myIdempotentAccessor")
#myIdempotentAccessor["spamandeggs"]
