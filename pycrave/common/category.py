from abc import ABC
from typing import Dict, List, Any


class Category(ABC):
    def __init__(self, type='', title='', image='', id=''):
        self.obj_type = 'category'
        self.type: str = type
        self.title: str = title
        self.image: str = image
        self.id: str = id

    @classmethod
    def from_args(cls, args):
        type = args['type'][0] if 'type' in args else ''
        title = args['title'][0] if 'title' in args else ''
        image = args['image'][0] if 'image' in args else ''
        id = args['id'][0] if 'id' in args else ''
        return cls(
            type=type,
            title=title,
            image=image,
            id=id
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'obj_type': self.obj_type,
            'type': self.type,
            'title': self.title,
            'image': self.image,
            'id': self.id,
        }

    def __str__(self) -> Dict[str, Any]:
        return str(self.__dict__)
