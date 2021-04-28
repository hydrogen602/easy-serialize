
# Easy-Serialize

Turn custom python objects into strings and vice-versa.

## Strengths

- no extra code to write
- supports json
- supports nested objects
- no dependencies outside of python's library (only pytest for developing)

## Drawbacks

- objects like tuples are automatically turned into lists
- only supports json right now
- can't handle circular references
- if an object has references in many places, it will be present in the json repeatedly and after deserializing will be separate objects
- Because of this, it cannot handle linked lists or similar interconnected data structures well
- stores `__dict__` of the object, so classes using `__slots__` likely won't work
- Because it needs to create the object and then copy over all the values of `__dict__`, it doesn't know the arguments used in `__init__`. Thus if the class requires arguments in `__init__`, the object will be created with `__new__` which avoids calling `__init__`. However, if `__init__` can take zero arguments, it will be called. A warning will be emitted if `__init__` is not called.

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
Serializable.serialize(object_to_serialize)
```

and deserialize using
```
Serializable.deserialize(stringified_object)
```