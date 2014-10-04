#!/usr/bin/env python
from ilwrathi import IdempotentAccessor

class myIdempotentAccessor(IdempotentAccessor):
    
    def get_spam(self):
        print "execing spam"
        return "spam"
    
    def get_eggs(self):
        print "execing eggs"
        return "eggs"

    def get_spamandeggs(self):
        print "execing baz"
        return "spam and eggs relies on %(spam)s and %(eggs)s" % self

#myIdempotentAccessor = myIdempotentAccessor("myIdempotentAccessor")
#myIdempotentAccessor["spamandeggs"]
