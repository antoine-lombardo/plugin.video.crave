from abc import ABC
from typing import Dict, List, Any
from urllib.parse import urlencode, parse_qs


class Category(ABC):
    def __init__(self, type='', title='', image='', id=''):
        self.obj_type = 'category'
        self.type: str = type
        self.title: str = title
        self.image: str = image
        self.id: str = id

    def to_url(self, base: str):
        return base + '?' + urlencode({
            "obj_type": self.obj_type,
            "cat_type": self.type,
            "id": self.id
        })

    @classmethod
    def from_url(cls, url: str):
        args = parse_qs(url[1:])
        obj = cls(
            type=args['cat_type'][0] if 'cat_type' in args else '',
            id=args['id'][0] if 'id' in args else ''
        )
        return obj

    def __str__(self) -> Dict[str, Any]:
        return str(self.__dict__)
