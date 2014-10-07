#!/usr/bin/env python2
from ._common.meta import _IACMeta

class IACBase(object):
    __metaclass__ = _IACMeta

    def iterkeys(self):
        """D.iterkeys() -> an iterator over the keys of D"""
        #This should be done with a metaclass
        return (k for k in self._keys)

    def itervalues(self):
        """D.values() -> list of D's values"""
        return (self[k] for k in self.iterkeys())
        
    def values(self):
        """D.values() -> list of D's values"""
        return [v for v in self.itervalues()]

    def iteritems(self):
        """D.iteritems() -> an iterator over the (key, value) items of D"""
        return ((k,v) for k,v in zip(self.iterkeys(), self.itervalues()))

    def items(self):
        """D.items() -> list of D's (key, value) pairs, as 2-tuples"""
        return [(k,v) for k,v in self.iteritems()]

    
