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
    def __init__(cls, name, bases, dct):
        #oh god
        old_init = cls.__init__
        def init(instance, *args, **kwargs):
            instance._cur_values = {}
            instance.history = []
            if not "name" in instance.__dict__:
                instance.name = "undefined"
            old_init(instance, *args, **kwargs)
        cls.__init__ = init
        super(_IACMeta, cls).__init__(name, bases, dct)
