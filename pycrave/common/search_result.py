from typing import List, Dict, Any


class SearchResult():

    def __init__(self, requirements=[], has_access=True, title='', search_title='', type='', description='', id='', image='', platform_tag='', version=None):
        self.obj_type = 'result'
        self.requirements: List[str] = requirements
        self.has_access: bool = has_access
        self.title: str = title
        self.search_title: str = search_title
        self.type: str = type
        self.description: str = description
        self.id: str = id
        self.image: str = image
        self.platform_tag: str = platform_tag
        self.version: str = version

    @classmethod
    def from_args(cls, args):
        requirements = args['requirements'][0] if 'requirements' in args else ''
        has_access = args['has_access'][0] if 'has_access' in args else ''
        title = args['title'][0] if 'title' in args else ''
        search_title = args['search_title'][0] if 'search_title' in args else ''
        type = args['type'][0] if 'type' in args else ''
        description = args['description'][0] if 'description' in args else ''
        id = args['id'][0] if 'id' in args else ''
        image = args['image'][0] if 'image' in args else ''
        platform_tag = args['platform_tag'][0] if 'platform_tag' in args else ''
        version = args['version'][0] if 'version' in args else None

        return cls(
            requirements=requirements,
            has_access=has_access,
            title=title,
            search_title=search_title,
            type=type,
            description=description,
            id=id,
            image=image,
            platform_tag=platform_tag,
            version=version
        )

    def to_dict(self):
        return {
            "obj_type": self.obj_type,
            "requirements": self.requirements,
            "has_access": self.has_access,
            "title": self.title,
            "search_title": self.search_title,
            "type": self.type,
            "description": self.description,
            "id": self.id,
            "image": self.image,
            "platform_tag": self.platform_tag
        }

    def __str__(self) -> Dict[str, Any]:
        return str(self.__dict__)

    def __lt__(self, other):
        if self.search_title != '':
            if(self.search_title < other.search_title):
                return True
            else:
                return False
        else:
            if(self.title < other.title):
                return True
            else:
                return False
