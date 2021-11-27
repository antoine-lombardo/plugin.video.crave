from abc import ABC
from typing import Dict, List, Any

from .media import Media


class ResultInfo():
    def __init__(self):
        self.obj_type = 'title'
        self.type: str = ''

        self.title: str = ''
        self.description: str = ''
        self.summary: str = ''
        self.image: str = ''

        self.medias: Dict[str, Media] = {}

    def __str__(self) -> Dict[str, Any]:
        return str(self.__dict__)


class MovieResultInfo(ResultInfo):
    def __init__(self):
        super().__init__()
        self.type = 'movie'
        self.year: int = year


class SerieResultInfo(ResultInfo):
    def __init__(self):
        super().__init__()
        self.type = 'serie'
