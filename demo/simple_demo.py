#!/usr/bin/env python
from ilwrath import Sac

class mySac(Sac):
    
    def get_spam(self):
        print "execing spam"
        return "spam"
    
    def get_eggs(self):
        print "execing eggs"
        return "eggs"

    def get_spamandeggs(self):
        print "execing baz"
        return "spam and eggs relies on %(spam)s and %(eggs)s" % self

#mysac = mySac("mysac")
#mysac["spamandeggs"]
