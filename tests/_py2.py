#!/usr/bin/env python2
from ilwrathi import IdempotentAccessor


class VerDepdIacTestClass(IdempotentAccessor):
    
    def setup(self):
        for k,v in self.__class__.__dict__.iteritems():
            if type(v) == types.FunctionType:
                self.__dict__[k + "_executed"] = False
        self._set_executed("setup")
