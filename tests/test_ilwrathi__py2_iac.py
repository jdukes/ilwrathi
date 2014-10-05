import unittest
import types

from rstr import word

from sys import path
path.insert(0,'..')
from ilwrathi import IdempotentAccessor

from sys import version_info as _version_info
if _version_info.major == 2:
    try:
        from ._py2 import _IACTestMetaClass
    except ValueError:
        path.insert(0,'.')
        from _py2 import _IACTestMetaClass

class IdempotentAccessorTestClass(IdempotentAccessor):
    __metaclass__ = _IACTestMetaClass

    def setup(self):
        for k,v in self.__class__.__dict__.iteritems():
            if type(v) == types.FunctionType:
                self.__dict__[k + "_executed"] = False
        self._set_executed("setup")

    def _set_executed(self, method):
        print "executing for method %s" % method
        self.__dict__[method+"_executed"] = True

    def get_uniquestr(self):
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
            self.assertIn(i,self.iac_foo._cur_values)

    def test___init__unique_test(self):
        iac_bar = IdempotentAccessorTestClass("bar")
        self.assertNotEquals(self.iac_foo["uniquestr"], 
                             iac_bar["uniquestr"])

    def test___init__setup_test(self):
        self.assertTrue(self.iac_foo.setup_executed)

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
        #why is this failing???
        self.iac_foo["spam"] = "ignored"
        self.assertTrue(self.iac_foo.set_spam_executed)

    def test___str__(self):
        self.assertEqual("foo", str(self.iac_foo))

    def test_clear(self):
        self.iac_foo.clear()
        self.assertEquals(self.iac_foo._cur_values, {})

    def test_items(self):
        #this test should check that the function blah.get_<key> is
        #the same as key for each key
        assert False
        #expected = self.iac_foo.items()
        #self.assertEqual(expected, self.iac_foo.items())

    def test_iteritems(self):
        #could use a better test
        assert False
        self.assertEqual(self.iac_foo.items(), 
                         [(k,v) for k,v in self.iac_foo.iteritems()])

    def test_iterkeys(self):
        # self.iac_foo = IdempotentAccessorTestClass(name, **kwargs)
        # self.assertEqual(expected, self.iac_foo.iterkeys())
        assert False # TODO: implement your test here

    def test_itervalues(self):
        # self.iac_foo = IdempotentAccessorTestClass(name, **kwargs)
        # self.assertEqual(expected, self.iac_foo.itervalues())
        assert False # TODO: implement your test here

    def test_keys(self):
        # dict( (k[4:],v) for k,v in iac.__class__.__dict__.iteritems() 
        #       if k.startswith("get_"))
        # self.iac_foo = IdempotentAccessorTestClass(name, **kwargs)
        # self.assertEqual(expected, self.iac_foo.keys())
        assert False # TODO: implement your test here

    def test_new(self):
        self.assertNotEqual(self.iac_foo.new("uniquestr"), self.iac_foo.new("uniquestr"))
        self.assertNotEqual(self.iac_foo.new("uniquestr"), self.iac_foo["uniquestr"])

    @unittest.skip("this idea isn't complete yet")
    def test_next(self):
        # self.iac_foo = IdempotentAccessorTestClass(name, **kwargs)
        # self.assertEqual(expected, self.iac_foo.next())
        assert False # TODO: implement your test here

    def test_values(self):
        # self.iac_foo = IdempotentAccessorTestClass(name, **kwargs)
        # self.assertEqual(expected, self.iac_foo.values())
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
