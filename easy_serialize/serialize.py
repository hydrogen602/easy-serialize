from typing import Dict, Literal
import json

class Serializable:
    __obj_register: Dict[str, type] = {}

    def __init__(self, *args, **kwargs) -> None:
        if type(self) is Serializable:
            raise Exception('Serializable can\'t be instantiated, just subclassed')
        super().__init__(*args, **kwargs)

    def __init_subclass__(cls) -> None:
        if cls.__qualname__ in Serializable.__obj_register:
            raise Exception(f'A class with the name "{cls.__qualname__}" already exists')
        Serializable.__obj_register[cls.__qualname__] = cls        

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
