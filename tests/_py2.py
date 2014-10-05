#!/usr/bin/env python2

class _IACTestMetaClass(type):

    def __new__(meta, name, bases, dct):
        update_dict = {}
        for i in dct:
            if i.startswith('get_'):
                update_dict[i + "_executed"] = False
                key = i[4:]
                for m in ["set_", "check_","del_"]:
                    meth = m + key
                    update_dict[meth] =  lambda c,*a: c._set_executed(meth)
                    update_dict[meth + "_executed"] = False
        dct.update(update_dict)
        return super(_IACTestMetaClass, meta).__new__(meta,
                                                      name,
                                                      bases,
                                                      dct)
