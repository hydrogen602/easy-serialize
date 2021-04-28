import sys
import pathlib
import json

p = pathlib.Path(sys.path[0]) / '..'
sys.path.append(str(p))
del p

def test_1():
    pass

def test_2():
    from easy_serialize.serialize import Serializable

    class A(Serializable):
        pass

def test_3():
    from easy_serialize.serialize import Serializable

    class A(Serializable):
        pass

    a = A()

    s = Serializable.serialize(a)
    assert json.loads(s) == {'_Serializable__class_id': 'test_3.<locals>.A'}