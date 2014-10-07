from types import FunctionType as _fntype

class _IACMeta(type):
    
    def __new__(meta, name, bases, dct):
        keys = [k[4:] for k,v in dct.items()
                if k.startswith('get_') and type(v) == _fntype]
        dct["_keys"] = keys
        return super(_IACMeta, meta).__new__(meta,
                                             name,
                                             bases,
                                             dct)

