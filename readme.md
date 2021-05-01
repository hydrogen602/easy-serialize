
# Easy-Serialize

Turn custom python objects into strings and vice-versa.

## Strengths

- no extra code to write in most cases
- supports json
- supports nested objects
- no dependencies outside of python's library (only pytest for developing)
- ability to add methods to control serializing and deserializing
- type hints and works with mypy

## Drawbacks

- objects like tuples are automatically turned into lists
- only supports json right now
- can't handle circular references
- if an object has references in many places, it will be present in the json repeatedly and after deserializing will be separate objects
- Because of this, it cannot handle linked lists or similar interconnected data structures well
- stores `__dict__` of the object, so classes using `__slots__` will likely require overriding the `serialize` method and `deserialize` classmethod.

## How to use

Extend `Serializable`
```
class A(Serializable):
    ...
```

or use the `make_serializable` decorator
```
@make_serializable
class A:
    ...
```

serialize using
```
serialize(object_to_serialize)
```

and deserialize using
```
deserialize(stringified_object)
```

### Custom serializing

In the case that the standard method doesn't cut it, it is
possible to add custom serializing and deserializing methods to a class

```
@make_serializable
class A:
    def __init__(self, x):
        self.x = x

    def serialize(self) -> dict:
        return {'x': self.x}
    
    @classmethod
    def deserialize(cls, data: dict) -> 'A':
        return A(data['x'])
```

## Notes

- `__init__` is by default not called for deserialized objects
    - Because it needs to create the object and then copy over all the values of `__dict__`, it doesn't know the arguments used in `__init__`. Thus if the class requires arguments in `__init__`, the object will be created with `__new__` which avoids calling `__init__`. However, if `__init__` can take zero arguments, it will be called. A warning will be emitted if `__init__` is not called.

## Future

Things to possibly add:
- other data formats like xml or the like
- support for objects with circular references
