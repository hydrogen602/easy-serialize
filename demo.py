from easy_serialize import make_serializable, Serializable, serialize, deserialize

# Using a decorator

@make_serializable
class Foo:

    def __init__(self, bar, baz) -> None:
        self.bar = bar
        self.baz = [baz, 42, "Hello World!"]
    
    def __str__(self) -> str:
        return f'Foo where bar = {self.bar} and baz = {self.baz}'
    
    __repr__ = __str__

f = Foo("Test", 3.1415)

print('f    =', f)

data = serialize(f)

print('data =', data)

f2 = deserialize(data)

print('f2   =', f2)
print()

# Using subclasses

class Foo2(Serializable):

    def __init__(self, bar, baz) -> None:
        self.bar = bar
        # also supports nested custom objects
        self.baz = [baz, Foo(1, True), "Hello World!"]
    
    def __str__(self) -> str:
        return f'Foo2 where bar = {self.bar} and baz = {self.baz}'

f = Foo2("Test", 3.1415)

print('f    =', f)

data = serialize(f)

print('data =', data)

f2 = deserialize(data)

print('f2   =', f2)