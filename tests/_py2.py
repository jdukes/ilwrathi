#!/usr/bin/env python2
import types

class _IACTestMetaClass(type):

    def __new__(meta, name, bases, dct):
        update_dict = {}
        for i in dct:
            if i.startswith('get_'):
                key = i[4:]
                for m in ["set_", "check_","del_"]:
                    meth = m + key
                    update_dict[meth] =  lambda c,*a: c._set_executed(meth,*a)
        dct.update(update_dict)
        cls =  super(_IACTestMetaClass, meta).__new__(meta,
                                                      name,
                                                      bases,
                                                      dct)
        return cls
    
                                
