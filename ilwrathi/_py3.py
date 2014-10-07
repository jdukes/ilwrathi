#!/usr/bin/env python3
from ._common.meta import _IACMeta

class IACBase(object, metaclass=_IACMeta):

    def values(self):
        """D.values() -> list of D's values"""
        return [self[k] for k in self.keys()]

    def items(self):
        """D.iteritems() -> an iterator over the (key, value) items of D"""
        #is this the behavior I want?
        return dict((k,v) for k,v in zip(self.keys(), self.values())).items()



