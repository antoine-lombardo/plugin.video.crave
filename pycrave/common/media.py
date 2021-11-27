from abc import ABC
import ast
from typing import Dict, List, Any


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

    def __str__(self) -> Dict[str, Any]:
        return str(self.__dict__)


class MediaMovie(Media):
    def __init__(self, title='', description='', summary='', image='', has_access=True, duration=0, playback_languages=[], play_id=''):
        super().__init__(title=title, description=description, summary=summary, image=image, has_access=has_access,
                         duration=duration, playback_languages=playback_languages, play_id=play_id)
        self.type: str = 'movie'

    @classmethod
    def from_args(cls, args):
        title = args['title'][0] if 'title' in args else ''
        description = args['description'][0] if 'description' in args else ''
        summary = args['summary'][0] if 'summary' in args else ''
        image = args['image'][0] if 'image' in args else ''
        has_access = args['has_access'][0] if 'has_access' in args else True
        duration = args['duration'][0] if 'duration' in args else 0
        playback_languages = ast.literal_eval(args['playback_languages'][0]) if 'playback_languages' in args else [
        ]
        play_id = args['play_id'][0] if 'play_id' in args else ''
        additionnal_infos = ast.literal_eval(args['additionnal_infos'][0]) if 'additionnal_infos' in args else {
        }

        obj = cls(
            title=title, description=description, summary=summary, image=image, has_access=has_access,
            duration=duration, playback_languages=playback_languages, play_id=play_id
        )
        obj.additionnal_infos = additionnal_infos
        return obj


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

    @classmethod
    def from_args(cls, args):
        season = int(args['season'][0]) if 'season' in args else -1
        episode = int(args['episode'][0]) if 'episode' in args else -1
        episode_tag = args['episode_tag'][0] if 'episode_tag' in args else ''

        title = args['title'][0] if 'title' in args else ''
        description = args['description'][0] if 'description' in args else ''
        summary = args['summary'][0] if 'summary' in args else ''
        image = args['image'][0] if 'image' in args else ''
        has_access = args['has_access'][0] if 'has_access' in args else 'True'
        if has_access == 'False':
            has_access = False
        else:
            has_access = True
        duration = args['duration'][0] if 'duration' in args else 0
        playback_languages = ast.literal_eval(args['playback_languages'][0]) if 'playback_languages' in args else [
        ]
        play_id = args['play_id'][0] if 'play_id' in args else ''
        additionnal_infos = ast.literal_eval(args['additionnal_infos'][0]) if 'additionnal_infos' in args else {
        }

        obj = cls(
            title=title, description=description, summary=summary, image=image, has_access=has_access,
            duration=duration, playback_languages=playback_languages, play_id=play_id, season=season, episode=episode, episode_tag=episode_tag
        )
        obj.additionnal_infos = additionnal_infos
        return obj
