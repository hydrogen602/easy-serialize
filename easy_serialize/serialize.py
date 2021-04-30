from typing import Dict, Literal, Optional, TypeVar
import json
import warnings

T = TypeVar('T')


def make_serializable(cls: T) -> T:
    '''
    Marks the class as being serializable
    '''
    if not isinstance(cls, type):
        raise TypeError(f'cls argument must be a class, got "{type(cls)}" instead')
    Serializable._register_new_class(cls)
    return cls


class Serializable:
    '''
    Subclasses this class to make classes serializable
    '''
    __obj_register: Dict[str, type] = {}

    def __init__(self, *args, **kwargs) -> None:
        if type(self) is Serializable:
            raise TypeError('Serializable can\'t be instantiated, just subclassed')
        super().__init__(*args, **kwargs)

    def serialize(self) -> dict:
        '''
        Method for implementing custom serialization. Overriding
        this method will cause this method to be used rather
        than copying `__dict__`
        '''
        if type(self) is Serializable:
            raise TypeError('Can\'t serialize "Serializable"')
    
    @classmethod
    def deserialize(cls, data: dict) -> 'Serializable':
        '''
        Method for implementing custom deserialization. Overriding
        this method will cause this method to be used rather
        than copying `__dict__`
        '''
        if cls is Serializable:
            raise TypeError('Can\'t deserialize "Serializable"')

    def __init_subclass__(cls) -> None:
        Serializable._register_new_class(cls)
        super().__init_subclass__()    

    @staticmethod
    def _register_new_class(cls_to_add) -> None:
        if cls_to_add.__qualname__ in Serializable.__obj_register and Serializable.__obj_register[cls_to_add.__qualname__] is not cls_to_add:
            raise Exception(f'A class with the name "{cls_to_add.__qualname__}" already exists')
        Serializable.__obj_register[cls_to_add.__qualname__] = cls_to_add

    @staticmethod
    def _get_class(class_name) -> Optional[type]:
        return Serializable.__obj_register.get(class_name)


def __sameFunctions(f, g):
    f = f.__func__ if hasattr(f, '__func__') else f
    g = g.__func__ if hasattr(g, '__func__') else g
    return f is g

    
def __convert_to_json_dict(obj: object) -> object:
    class_name = type(obj).__qualname__
    #print(class_name)
    if Serializable._get_class(class_name) is None:
        #print(Serializable._get_class(class_name), Serializable._Serializable__obj_register[class_name])
        raise Exception(f'Class "{class_name}" is not serializable')
    
    if hasattr(obj, 'serialize') and not __sameFunctions(obj.serialize, Serializable.serialize):
        data = obj.serialize()
        if not isinstance(data, dict):
            raise TypeError(f'Method "serialize" of class "{type(obj).__qualname__}" should return a dict, but instead returned "{type(data)}"')
    
    else:
        data = obj.__dict__.copy()

    data['_Serializable__class_id'] = class_name
    return data


def __convert_from_json_dict(obj: object, ignore_init_issue: bool = False) -> object:
    if isinstance(obj, dict) and '_Serializable__class_id' in obj:
        class_name = obj['_Serializable__class_id']

        class_ = Serializable._get_class(class_name)
        if class_ is None:
            raise Exception(f'Class "{class_name}" is not deserializable')
        del obj['_Serializable__class_id']

        if hasattr(class_, 'deserialize') and not __sameFunctions(class_.deserialize, Serializable.deserialize):
            print(class_.deserialize, class_)
            new_obj = class_.deserialize(obj)
            if not isinstance(new_obj, class_):
                raise TypeError(f'Method "deserialize" of class "{class_.__qualname__}" should return an instance of itself, but instead returned "{type(new_obj)}"')
        else:
            try:
                # try creating the object with init
                new_obj = class_()
            except TypeError:
                if not ignore_init_issue:
                    warnings.warn(f'Class "{class_name}" couldn\'t be created using __init__ , thus it will be created without calling __init__. Consider allowing __init__ to take no arguments')
                new_obj = class_.__new__(class_)

            new_obj.__dict__ = obj # copy over all the data

        return new_obj

    return obj

    
def serialize(obj: 'Serializable', method: Literal['json'] = 'json') -> str:
    if method == 'json':
        data = __convert_to_json_dict(obj)
        return json.dumps(data, default=__convert_to_json_dict)
    else:
        raise ValueError(f'Unknown method: "{method}"')


def deserialize(data: str, method: Literal['json'] = 'json', ignore_init_issue: bool = False) -> str:
    if method == 'json':
        def f(*args, **kwargs):
            return __convert_from_json_dict(*args, **kwargs, ignore_init_issue=ignore_init_issue)

        return json.loads(data, object_hook=f)
    else:
        raise ValueError(f'Unknown method: "{method}"')