#!/usr/bin/env python
from eggsac import Sac

class LookAtMySac(Sac):
    
    def get_spam(self):
        print "execing spam"
        return "spam"
    
    def get_eggs(self):
        print "execing eggs"
        return "eggs"

    def get_spamandeggs(self):
        print "execing baz"
        return "spam and eggs relies on %(spam)s and %(eggs)s" % self

#mysac = LookAtMySac("mysac")
#mysac["spamandeggs"]
