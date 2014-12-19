#!/usr/bin/env python
#TODO: add verbose messages for each assert to describe why
#TODO: add doctests
import unittest
import types
import inspect

from rstr import word
from sys import path, version_info

from ilwrathi import IdempotentAccessor


class IdempotentAccessorTestClass(IdempotentAccessor):
    #need an actual set, check, del

    def __init__(self, name=None, *args, **kwargs):
        def mk_exec_setter(meth):
            def func(*args):
                self._set_executed(meth)
                return True
            return func
        self.name = name
        for key in self._keys:
                for m in ["set_", "check_","del_"]:
                    meth = m + key
                    #lambda didn't work... no idea why. look in to this
                    attr = getattr(self, meth, None)
                    setattr(self, meth, attr or mk_exec_setter(meth))
                    setattr(self, meth + "_executed", False)
                setattr(self, key + "_executed", False)
        self.my_init_executed = True

    def _set_executed(self, method):
        #print "executing for method %s" % method
        setattr(self, method+"_executed", True)

    def get_spam(self):
        self._get_spam_executed = True
        return "spam"

    def get_eggs(self):
        self._get_eggs_executed = True
        return "eggs"

    def get_spamandeggs(self):
        self._get_spamandeggs_executed = True
        return "spam and eggs relies on %(spam)s and %(eggs)s" % self

    def get_zfailing(self):
        self._get_zfailing_executed = True
        return word(10)

    def check_zfailing(self, val):
        return False

    def get_uniquestr(self):
        self._get_uniquestr_executed = True
        return word(10)


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
        self.assertNotEqual(old_unique, self.iac_foo["uniquestr"])
        with self.assertRaises(KeyError):
            del(self.iac_foo["badkey"])

    def test___getitem__(self):
        self.assertEqual("spam and eggs relies on spam and eggs", 
                         self.iac_foo["spamandeggs"])
        self.assertTrue(self.iac_foo._get_spamandeggs_executed)
        self.assertTrue(self.iac_foo._get_spam_executed)
        self.assertTrue(self.iac_foo._get_eggs_executed)
        for i in ["spam","eggs","spamandeggs"]:
            self.assertIn(i, self.iac_foo._cur_values)
            func = getattr(self.iac_foo,"get_" + i)
            self.assertEqual(self.iac_foo[i],
                              func())
        f = self.iac_foo["zfailing"]
        self.assertNotEquals(f,self.iac_foo["zfailing"])
        with self.assertRaises(KeyError):
            self.iac_foo["badkey"]

    def test___init__test(self):
        self.assertTrue(self.iac_foo.my_init_executed, 
                        msg="setup failed to execute")
        iac_bar = IdempotentAccessorTestClass("bar")
        self.assertNotEqual(self.iac_foo["uniquestr"], 
                            iac_bar["uniquestr"],
                            msg="intsances are not unique")
        self.assertEqual(iac_bar.name,"bar")

    @unittest.skipIf(version_info.major < 3, 
                     "This is a pain in the ass on py2")
    def test___init__funcdef_test(self):
        s = inspect.signature(self.iac_foo.__init__)
        self.assertIn("name", s.parameters)

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
        with self.assertRaises(KeyError):
            self.iac_foo["badkey"] = "ignored"

    def test___str__(self):
        self.assertEqual("foo", str(self.iac_foo))

    def test_clear(self):
        self.iac_foo.clear()
        self.assertEqual(self.iac_foo._cur_values, {})

    def test_items(self):
        expected = [('eggs', 'eggs'),
                    ('spamandeggs', 'spam and eggs relies on spam and eggs'),
                    ('spam', 'spam')]
        self.assertEqual(sorted(expected), sorted(self.iac_foo.items())[:-2])

    @unittest.skipIf(version_info.major == 3, "iter unneeded on 3")
    def test_iteritems(self):
        items = [i for i in self.iac_foo.items() if not i[0] == 'zfailing']
        iteritems = [(k,v) for k,v in self.iac_foo.iteritems() 
                     if not k =='zfailing']
        self.assertEqual(items, iteritems)
        

    @unittest.skipIf(version_info.major == 3, "iter unneeded on 3")
    def test_iterkeys(self):
        self.assertEqual(sorted(self.iac_foo._keys), 
                         sorted([k for k in self.iac_foo.iterkeys()]), 
                         msg="keys are missing")

    @unittest.skipIf(version_info.major == 3, "iter unneeded on 3")
    def test_itervalues(self):
        assert not self.iac_foo._cur_values, "test setup falid"
        expected = ['eggs', 'spam and eggs relies on spam and eggs', 'spam']
        msg = "values didn't match the expected set"
        values = [v for v in self.iac_foo.itervalues()]
        for e in expected:
            self.assertIn(e, values)
        for k in self.iac_foo.keys():
            variable = "_get_" + k + "_executed"
            executed = self.iac_foo.__dict__[variable]
            self.assertTrue(executed, msg="%s was %s" % (variable, executed))
        #this test is fucking wrong
        msg = "Two execs should always return the same value set"
        run_one = sorted([v for v in self.iac_foo.itervalues()][:-3])
        run_two = sorted([v for v in self.iac_foo.itervalues()][:-3])
        self.assertEqual(run_one[:-1], run_two[:-1],msg=msg)

    def test_keys(self):
        items = self.iac_foo.__class__.__dict__.items() 
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
        with self.assertRaises(KeyError):
            self.iac_foo.new("notexists")

    @unittest.skip("this idea isn't complete yet")
    def test_next(self):
        # self.iac_foo = IdempotentAccessorTestClass(name, **kwargs)
        # self.assertEqual(expected, self.iac_foo.next())
        assert False # TODO: implement your test here

    def test_values(self):
        assert not self.iac_foo._cur_values, "test setup falid"
        expected = ['eggs', 'spam and eggs relies on spam and eggs', 'spam']
        msg = "values didn't match the expected set"
        for e in expected:
            self.assertIn(e, self.iac_foo.values(), msg=msg)
        for i in ["spam","eggs","spamandeggs","uniquestr"]:
            functionname = "_get_" + i + "_executed"
            executed = self.iac_foo.__dict__[functionname]
            self.assertTrue(executed, msg="%s didn't execute" % functionname)

    def test__setattr__(self):
        setattr(self.iac_foo, "get_test",lambda cls: "test")
        self.assertIn("test", self.iac_foo.keys())
        self.assertEqual("test", self.iac_foo["test"])
        delattr(self.iac_foo, "get_test")


if __name__ == '__main__':
    unittest.main()
