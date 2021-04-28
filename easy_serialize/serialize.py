from typing import Dict, Literal, TypeVar
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
            raise Exception('Serializable can\'t be instantiated, just subclassed')
        super().__init__(*args, **kwargs)

    def __init_subclass__(cls) -> None:
        Serializable._register_new_class(cls)
        super().__init_subclass__()    

    @staticmethod
    def _register_new_class(cls_to_add) -> None:
        if cls_to_add.__qualname__ in Serializable.__obj_register and Serializable.__obj_register[cls_to_add.__qualname__] is not cls_to_add:
            raise Exception(f'A class with the name "{cls_to_add.__qualname__}" already exists')
        Serializable.__obj_register[cls_to_add.__qualname__] = cls_to_add

    @classmethod
    def __convert_to_json_dict(cls, obj: object) -> object:
        class_name = type(obj).__qualname__
        if class_name not in cls.__obj_register:
            raise Exception(f'Class "{class_name}" is not serializable')

        data = obj.__dict__.copy()
        data['_Serializable__class_id'] = class_name
        return data

    @classmethod
    def serialize(cls, obj: 'Serializable', method: Literal['json'] = 'json') -> str:
        if method == 'json':
            data = cls.__convert_to_json_dict(obj)
            return json.dumps(data, default=cls.__convert_to_json_dict)
        else:
            raise ValueError(f'Unknown method: "{method}"')

    @classmethod
    def __convert_from_json_dict(cls, obj: object, ignore_init_issue: bool = False) -> object:
        if isinstance(obj, dict) and '_Serializable__class_id' in obj:
            class_name = obj['_Serializable__class_id']
            if class_name not in cls.__obj_register:
                raise Exception(f'Class "{class_name}" is not deserializable')

            class_ = cls.__obj_register[class_name]
            del obj['_Serializable__class_id']

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

    @classmethod
    def deserialize(cls, data: str, method: Literal['json'] = 'json', ignore_init_issue: bool = False) -> str:
        if method == 'json':
            def f(*args, **kwargs):
                return cls.__convert_from_json_dict(*args, **kwargs, ignore_init_issue=ignore_init_issue)

            return json.loads(data, object_hook=f)
        else:
            raise ValueError(f'Unknown method: "{method}"')
