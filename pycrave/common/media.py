from abc import ABC
import ast
from typing import Dict, List, Any
from urllib.parse import urlencode, parse_qs


class Media():
    def __init__(self, title='', description='', summary='', image='', has_access=True, duration=0, playback_languages=[], play_id=''):
        self.obj_type = 'media'
        self.type: str = ''

        self.title: str = title
        self.description: str = description
        self.summary: str = summary
        self.image: str = image
        self.has_access: bool = has_access

        self.duration: int = duration
        self.playback_languages: List[str] = playback_languages

        self.play_id: Dict[str, str] = play_id
        self.additionnal_infos: Dict[str, Any] = {}

    def to_dict(self):
        return {
            "obj_type": self.obj_type,
            "type": self.type,
            "title": self.title,
            "has_access": self.has_access,
            "description": self.description,
            "summary": self.summary,
            "image": self.image,
            "duration": self.duration,
            "playback_languages": self.playback_languages,
            "play_id": self.play_id,
            "additionnal_infos": self.additionnal_infos
        }

    def to_url(self, base: str):
        return base + '?' + urlencode({
            "obj_type": self.obj_type,
            "id": self.play_id,
            "dest": self.additionnal_infos['destination'],
            "lang": self.playback_languages[0],
        })

    @classmethod
    def from_url(cls, url: str):
        args = parse_qs(url[1:])
        obj = cls(
            playback_languages=[args['lang'][0]] if 'lang' in args else [],
            play_id=args['id'][0] if 'id' in args else '')
        obj.additionnal_infos = {'destination':
                                 args['dest'][0]} if 'dest' in args else {}
        return obj

    def __str__(self) -> Dict[str, Any]:
        return str(self.__dict__)


class MediaMovie(Media):
    def __init__(self, title='', description='', summary='', image='', has_access=True, duration=0, playback_languages=[], play_id=''):
        super().__init__(title=title, description=description, summary=summary, image=image, has_access=has_access,
                         duration=duration, playback_languages=playback_languages, play_id=play_id)
        self.type: str = 'movie'


class MediaEpisode(Media):
    def __init__(self, title='', description='', summary='', image='', has_access=True, duration=0, playback_languages=[], play_id='', season=-1, episode=-1, episode_tag=''):
        super().__init__(title=title, description=description, summary=summary, image=image, has_access=has_access,
                         duration=duration, playback_languages=playback_languages, play_id=play_id)
        self.type: str = 'episode'
        self.season: str = season
        self.episode: str = episode
        self.episode_tag: str = episode_tag

    def to_dict(self):
        return {
            "season": self.season,
            "episode": self.episode,
            "episode_tag": self.episode_tag,
            "obj_type": self.obj_type,
            "type": self.type,
            "title": self.title,
            "has_access": self.has_access,
            "description": self.description,
            "summary": self.summary,
            "image": self.image,
            "duration": self.duration,
            "playback_languages": self.playback_languages,
            "play_id": self.play_id,
            "additionnal_infos": self.additionnal_infos
        }
