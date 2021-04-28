import sys
import pathlib
import json
import pytest

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

def test_4():
    from easy_serialize.serialize import Serializable

    class A(Serializable):
        
        def __init__(self, x, y) -> None:
            self.x = x
            self.__y = y

    a = A(5.3, [1, 'hi'])

    s = Serializable.serialize(a)
    assert json.loads(s) == {'_Serializable__class_id': 'test_4.<locals>.A', 'x': 5.3, '_A__y': [1, 'hi']}

def test_5():
    from easy_serialize.serialize import Serializable

    class B(Serializable):
        def __init__(self) -> None:
            self.foo = 1
    class A(Serializable):
        
        def __init__(self, x) -> None:
            self.x = x
            self.__y = B()

    a = A(5.3)

    s = Serializable.serialize(a)
    assert json.loads(s) == {'_Serializable__class_id': 'test_5.<locals>.A', 'x': 5.3, '_A__y': {'_Serializable__class_id': 'test_5.<locals>.B', 'foo': 1}}

def test_6():
    from easy_serialize.serialize import Serializable

    class B:
        def __init__(self) -> None:
            self.foo = 1
    class A(Serializable):
        
        def __init__(self, x) -> None:
            self.x = x
            self.__y = B()
    
    with pytest.raises(Exception):
        Serializable.serialize(A(5))
    
    with pytest.raises(Exception):
        Serializable.serialize(B())

def test_7():
    from easy_serialize.serialize import Serializable

    class A(Serializable):
        def __init__(self, x, *args) -> None:
            self.x = x
            self.__y =  list(args)
        def __eq__(self, o: object) -> bool:
            if isinstance(o, A):
                return o.x == a.x and o.__y == self.__y
    
    a = A(3.14, 'hello', 'world')

    s = Serializable.serialize(a)

    a_changed = Serializable.deserialize(s, ignore_init_issue=True)

    assert a == a_changed


def test_7():
    from easy_serialize.serialize import Serializable

    class B(Serializable):
        def __init__(self, data = None) -> None:
            self.data = list(data)
        def __eq__(self, o: object) -> bool:
            return isinstance(o, B) and o.data == self.data

    class A(Serializable):
        def __init__(self, x, *args) -> None:
            self.x = x
            self.__y =  B(args)
        def __eq__(self, o: object) -> bool:
            return isinstance(o, A) and o.x == a.x and o.__y == self.__y
    
    a = A(3.14, 'hello', 'world')

    s = Serializable.serialize(a)

    a_changed = Serializable.deserialize(s, ignore_init_issue=True)

    # assert a.x == a_changed.x
    # print(a._A__y.data)
    # print(a_changed._A__y.data)
    # assert a._A__y == a_changed._A__y
    assert a == a_changed
