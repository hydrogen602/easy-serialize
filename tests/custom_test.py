import sys
import pathlib
import json
import pytest

p = str(pathlib.Path(sys.path[0]) / '..')
if p not in sys.path:
    sys.path.append(p)
del p


def test_custom_1():
    from easy_serialize import Serializable

    with pytest.raises(TypeError):
        Serializable()
    
    with pytest.raises(TypeError):
        Serializable.deserialize({})

def test_custom_2():
    from easy_serialize import Serializable, serialize, deserialize

    class A(Serializable):
        def __init__(self, x, y) -> None:
            self.x = x
            self.y = y

        def serialize(self) -> dict:
            return {'x': self.x}
        
        @classmethod
        def deserialize(cls, data: dict) -> 'Serializable':
            return A(data['x'], 'recreated')
    
    a = A(42, 'original')

    b = deserialize(serialize(a))

    assert a.x == b.x
    assert a.y == 'original'
    assert b.y == 'recreated'

def test_custom_3():
    from easy_serialize import make_serializable, serialize, deserialize

    @make_serializable
    class A:
        def __init__(self, x, y) -> None:
            self.x = x
            self.y = y

        def serialize(self) -> dict:
            return {'x': self.x}
        
        @classmethod
        def deserialize(cls, data: dict) -> 'A':
            return A(data['x'], 'recreated')
    
    a = A(42, 'original')

    b = deserialize(serialize(a))

    assert a.x == b.x
    assert a.y == 'original'
    assert b.y == 'recreated'