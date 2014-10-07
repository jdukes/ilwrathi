#!/usr/bin/env python
#TODO: add verbose messages for each assert to describe why

import unittest
import types

from rstr import word

from sys import path, version
path.insert(0,'..')
from ilwrathi import IdempotentAccessor


def mk_exec_setter(meth):
    def func(cls, *args):
        cls._set_executed(meth)
        return True
    return func


class _MetaTestClass(type):

    def __new__(meta, name, bases, dct):
        update_dict = {}
        for i in dct:
            if i.startswith('get_'):
                key = i[4:]
                for m in ["set_", "check_","del_"]:
                    meth = m + key
                    #lambda didn't work... no idea why. look in to this
                    update_dict[meth] = mk_exec_setter(meth)
        dct.update(update_dict)
        cls = super(_MetaTestClass, meta).__new__(meta,
                                                  name,
                                                  bases,
                                                  dct)
        return cls


class IdempotentAccessorTestClass(IdempotentAccessor):
    __metaclass__ = _MetaTestClass

    def _set_executed(self, method):
        #print "executing for method %s" % method
        setattr(self, method+"_executed", True)
    
    def setup(self):
        for k,v in self.__class__.__dict__.items():
            if type(v) == types.FunctionType:
                setattr(self, k + "_executed", False)
        self.setup_executed = True

    def get_uniquestr(self):
        self.get_uniquestr_executed = True
        return word(10)

    def get_spam(self):
        self.get_spam_executed = True
        return "spam"

    def get_eggs(self):
        self.get_eggs_executed = True
        return "eggs"

    def get_spamandeggs(self):
        self.get_spamandeggs_executed = True
        return "spam and eggs relies on %(spam)s and %(eggs)s" % self


class TestIdempotentAccessor(unittest.TestCase):

    def setUp(self):
        self.iac_foo = IdempotentAccessorTestClass("foo")
        
    def test___add__(self):
        self.assertEqual("foobar", self.iac_foo + "bar")

    def test___delitem__(self):
        self.iac_foo["spamandeggs"]
        self.assertFalse(self.iac_foo.del_spamandeggs_executed)
        del(self.iac_foo["spamandeggs"])
        self.assertTrue(self.iac_foo.del_spamandeggs_executed)
        self.assertNotIn("spamandeggs",self.iac_foo._cur_values)
        self.assertIn("spam",self.iac_foo._cur_values)
        old_unique = self.iac_foo["uniquestr"]
        del(self.iac_foo["uniquestr"])
        self.assertNotEquals(old_unique, self.iac_foo["uniquestr"])

    def test___getitem__(self):
        self.assertEqual("spam and eggs relies on spam and eggs", 
                         self.iac_foo["spamandeggs"])
        self.assertTrue(self.iac_foo.get_spamandeggs_executed)
        self.assertTrue(self.iac_foo.get_spam_executed)
        self.assertTrue(self.iac_foo.get_eggs_executed)
        for i in ["spam","eggs","spamandeggs"]:
            self.assertIn(i, self.iac_foo._cur_values)
            func = getattr(self.iac_foo,"get_" + i)
            self.assertEquals(self.iac_foo[i],
                              func())

    def test___init__test(self):
        self.assertTrue(self.iac_foo.setup_executed, 
                        msg="setup failed to execute")
        iac_bar = IdempotentAccessorTestClass("bar")
        self.assertNotEquals(self.iac_foo["uniquestr"], 
                             iac_bar["uniquestr"],
                             msg="instances are not unique")

    @unittest.skip("this idea isn't complete yet")
    def test___iter__(self):
        # self.assertEqual(expected, idempotent_accessor.__iter__())
        assert False # TODO: implement your test here

    def test___radd__(self):
        self.assertEqual("barfoo", "bar" + self.iac_foo)

    def test___repr__(self):
        values = self.iac_foo.values()
        comp = "<IdempotentAccessorTestClass '%s': %s>" % (self.iac_foo.name, 
                                                           self.iac_foo._cur_values)
        self.assertEqual(comp, repr(self.iac_foo))

    def test___setitem__(self):
        self.iac_foo["spam"] = "ignored"
        self.assertTrue(self.iac_foo.set_spam_executed)

    def test___str__(self):
        self.assertEqual("foo", str(self.iac_foo))

    def test_clear(self):
        self.iac_foo.clear()
        self.assertEquals(self.iac_foo._cur_values, {})

    def test_items(self):
        expected = [('eggs', 'eggs'),
                    ('spamandeggs', 'spam and eggs relies on spam and eggs'),
                    ('spam', 'spam')]
        self.assertEqual(sorted(expected), sorted(self.iac_foo.items())[:-1])

    def test_iteritems(self):
        self.assertEqual(self.iac_foo.items(), 
                         [(k,v) for k,v in self.iac_foo.iteritems()])

    def test_iterkeys(self):
        items = self.iac_foo.__class__.__dict__.iteritems() 
        expected = dict( (k[4:],v) for k,v in items 
                         if k.startswith("get_")
                         and type(v) == types.FunctionType)
        self.assertEqual(sorted(expected.keys()), 
                         sorted([k for k in self.iac_foo.iterkeys()]), 
                         msg="keys are missing")

    @unittest.skipIf(
    def test_itervalues(self):
        assert not self.iac_foo._cur_values, "test setup falid"
        expected = ['eggs', 'spam and eggs relies on spam and eggs', 'spam']
        msg = "values didn't match the expected set"
        self.assertEqual(sorted(expected), 
                         sorted([v for v in self.iac_foo.itervalues()][:-1]))
        [ v for v in self.iac_foo.itervalues()]
        for k in self.iac_foo.keys():
            variable = "get_" + k + "_executed"
            executed = self.iac_foo.__dict__[variable]
            self.assertTrue(executed, msg="%s was %s" % (variable, executed))
        msg = "Two execs should always return the same value set"
        self.assertEqual(sorted([v for v in self.iac_foo.itervalues()]),
                         sorted([v for v in self.iac_foo.itervalues()]),
                         msg=msg)        

    def test_keys(self):
        items = self.iac_foo.__class__.__dict__.iteritems() 
        expected = dict( (k[4:],v) for k,v in items 
                         if k.startswith("get_")
                         and type(v) == types.FunctionType)
        self.assertEqual(sorted(expected.keys()),
                         sorted(self.iac_foo.keys()),
                         msg="keys are missing")

    def test_new(self):
        self.assertNotEqual(self.iac_foo.new("uniquestr"), 
                            self.iac_foo.new("uniquestr"))
        self.assertNotEqual(self.iac_foo.new("uniquestr"), 
                            self.iac_foo["uniquestr"])

    @unittest.skip("this idea isn't complete yet")
    def test_next(self):
        # self.iac_foo = IdempotentAccessorTestClass(name, **kwargs)
        # self.assertEqual(expected, self.iac_foo.next())
        assert False # TODO: implement your test here

    def test_values(self):
        assert not self.iac_foo._cur_values, "test setup falid"
        expected = ['eggs', 'spam and eggs relies on spam and eggs', 'spam']
        msg = "values didn't match the expected set"
        self.assertEqual(sorted(expected),
                         sorted(self.iac_foo.values()[:-1]), msg=msg)
        for i in ["spam","eggs","spamandeggs","uniquestr"]:
            functionname = "get_" + i + "_executed"
            executed = self.iac_foo.__dict__[functionname]
            self.assertTrue(executed, msg="%s didn't execute" % functionname)
        msg = "Two execs should always return the same value set"
        self.assertEqual(self.iac_foo.values(), self.iac_foo.values(), msg=msg)
                         
        

if __name__ == '__main__':
    unittest.main()