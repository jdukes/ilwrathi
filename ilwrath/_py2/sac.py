#!/usr/bin/env python2
#TODO: serialization

class Sac(object):
    """The Sac base class is a state independant store for values.

    This class acts like a dictionary. When a key is referenced, the
    Sac will check for the key in it's current state, optionally check
    that the value for the key is still valid, and return the value if
    it exists. If the value for the key is nonexistant or invalid, the
    Sac will attempt to update the value.

    The primary use case for this is in web service pen
    testing. Testing some service may require several unique objects
    to exist, which all have to be referenced together. The actual
    values of those references may be irrelevant for some testing. A
    hacker wants to focus on the important areas, letting the system
    maintain everything else. A Sac does this by allowing you to set
    up chained dependancies and automatically resolving them.

    To use a Sac, subclass it. Create get_<key> functions that return
    the values for keys. This is illustrated by the simple_demo.py in
    the demo directory:

    from ilwrath import Sac

    class LookAtMySac(Sac):
    
    def get_spam(self):
        print "execing spam"
        return "spam"
    
    def get_eggs(self):
        print "execing eggs"
        return "eggs"

    def get_spamandeggs(self):
        print "execing baz"
        return "spam and eggs relies on %(spam)s and %(eggs)s" % self

    And here's how it works:

    In [1]: mysac = LookAtMySac("mysac")

    In [2]: mysac
    Out[2]: <LookAtMySac 'mysac': {}>

    In [3]: mysac["spamandeggs"]
    execing baz
    execing spam
    execing eggs
    Out[3]: 'spamandeggs relies on spam and eggs'

    In [4]: mysac
    Out[4]: <LookAtMySac 'mysac': {'eggs': 'eggs', 'spamandeggs': 'baz relies on spam and eggs', 'spam': 'spam'}>

    In [5]: mysac["eggs"]
    Out[5]: 'eggs'

    In [6]: "as a string it looks like: " + mysac
    Out[6]: 'as a string it looks like: mysac'

    """ 
    
    def __init__(self, name=None, **kwargs):
        self.name = name
        self._cur_values = {}
        self.history = []
        if '_setup' in self.__class__.__dict__:
            #get function sig of _setup if exists and merge with func
            #sig of init
            self._setup(**kwargs)

    def __getitem__(self, key):
        if key in self._cur_values:
            value = self._cur_values[key]
            if  "validate" in self.__class__.__dict__:
                if not self.validate(key, value):
                    return self._get_and_update_entry(key)
            return value
        else:
            try:
                return self._get_and_update_entry(key)
            except KeyError:
                raise KeyError(key)

    def new(self, key):
        """Returns a unique item"""
        try:
            val =  self.__class__.__dict__["get_" + key](self)
            self.history.append(val)
            return val
        except KeyError:
            raise KeyError(key)

    def _get_and_update_entry(self, key):
        self._archive_vals()
        val = self.__class__.__dict__["get_" + key](self)
        self._cur_values[key] = val
        return val

    def __setitem__(self, key, value):
        self._archive_vals()
        self._cur_values[key] = val

    def __delitem__(self, key):
        self._archive_vals()
        del(self._cur_values[key])

    def __str__(self):
        return self.name

    def __iter__(self):
        return self

    def next(self):
        self.clear()
        return self

    def __add__(self, other):
        return self.name + other

    def __radd__(self, other):
        return other + self.name
        
    def get_history(self):
        return self.history
        
    def __repr__(self):
        return "<%s '%s': %s>" % (self.__class__.__name__,
                                  self.name,
                                  str(self._cur_values))

    def clear(self):
        self._archive_vals()
        self._cur_values = {}

    def _archive_vals(self):
        if self._cur_values:
            self.history.append(dict(self._cur_values))
