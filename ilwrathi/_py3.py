#!/usr/bin/env python3
from ._common.meta import _IACMeta
from inspect import signature

class _IACMetaPy3(_IACMeta):
    
    def __init__(cls, name, bases, dct):
        old_init = cls.__init__
        def init(self, *args, **kwargs):
            self._cur_values = {}
            self.history = []
            self.name = kwargs.get("name") or "undefined"
            old_init(self, *args, **kwargs)
        init.__signature__ = signature(old_init)
        cls.__init__ = init
        super(_IACMeta, cls).__init__(name, bases, dct)


class IACBase(object, metaclass=_IACMetaPy3):

    def values(self):
        """D.values() -> list of D's values"""
        return [self[k] for k in self.keys()]

    def items(self):
        """D.iteritems() -> an iterator over the (key, value) items of D"""
        #is this the behavior I want?
        return dict((k,v) for k,v in zip(self.keys(), self.values())).items()



