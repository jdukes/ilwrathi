import unittest

from sys import path
path.insert(0,'..')
from ilwrathi import IdempotentAccessor

from sys import version_info as _version_info
if _version_info.major == 2:
    from ._py2 import _IACTestMetaClass

class IdempotentAccessorTestClass(IdempotentAccessor):
    __metaclass__ = _IACTestMetaClass

    def _set_executed(self, method):
        self.__dict__[method+"_executed"] = True

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

    def test___add__(self):
        idempotent_accessor = IdempotentAccessor("foo")
        self.assertEqual("foobar", idempotent_accessor + "bar")

    def test___delitem__(self):
        idempotent_accessor = IdempotentAccessorTestClass("spamtest")
        idempotent_accessor["spamandeggs"]
        del(idempotent_accessor["spamandeggs"])
        self.assertNotIn("spamandeggs",idempotent_accessor._cur_values)
        self.assertIn("spam",idempotent_accessor._cur_values)
        self.assertTrue(idempotent_accessor.del_spamandeggs_executed)

    def test___getitem__(self):
        idempotent_accessor = IdempotentAccessorTestClass("spamtest")
        self.assertEqual("spamandeggs", idempotent_accessor["spamandeggs"])
        self.assertTrue(idempotent_accessor.get_spamandeggs_executed)
        self.assertTrue(idempotent_accessor.get_spam_executed)
        self.assertTrue(idempotent_accessor.get_eggs_executed)
        for i in ["spam","eggs","spamandeggs"]:
            self.assertIn(i,idempotent_accessor._cur_values)

    def test___init__(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        assert False # TODO: implement your test here

    def test___iter__(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.__iter__())
        assert False # TODO: implement your test here

    def test___radd__(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.__radd__(other))
        assert False # TODO: implement your test here

    def test___repr__(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.__repr__())
        assert False # TODO: implement your test here

    def test___setitem__(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.__setitem__(key, value))
        assert False # TODO: implement your test here

    def test___str__(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.__str__())
        assert False # TODO: implement your test here

    def test_clear(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.clear())
        assert False # TODO: implement your test here

    def test_items(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.items())
        assert False # TODO: implement your test here

    def test_iteritems(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.iteritems())
        assert False # TODO: implement your test here

    def test_iterkeys(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.iterkeys())
        assert False # TODO: implement your test here

    def test_itervalues(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.itervalues())
        assert False # TODO: implement your test here

    def test_keys(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.keys())
        assert False # TODO: implement your test here

    def test_new(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.new(key))
        assert False # TODO: implement your test here

    def test_next(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.next())
        assert False # TODO: implement your test here

    def test_values(self):
        # idempotent_accessor = IdempotentAccessor(name, **kwargs)
        # self.assertEqual(expected, idempotent_accessor.values())
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
