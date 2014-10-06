#!/usr/bin/env python2
import types

def mk_exec_setter(meth):
    return lambda c, *args: c._set_executed(meth)

class _IACTestMetaClass(type):
    

    def __new__(meta, name, bases, dct):
        update_dict = {}
        for i in dct:
            if i.startswith('get_'):
                key = i[4:]
                for m in ["set_", "check_","del_"]:
                    meth = m + key
                    #lambda didn't work... no idea why. look in to this
                    update_dict[meth] = mk_exec_setter(meth)
        print update_dict
        dct.update(update_dict)
        cls =  super(_IACTestMetaClass, meta).__new__(meta,
                                                      name,
                                                      bases,
                                                      dct)
        return cls
    
                                