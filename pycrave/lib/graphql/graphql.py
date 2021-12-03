from copy import deepcopy
from datetime import datetime
import json
import copy

from pycrave.common.category import Category

from ...common.media import MediaEpisode, MediaMovie
from ...common.result_info import ResultInfo, SerieResultInfo, MovieResultInfo
from ...common.search_result import SearchResult
from ...common.utils import format_episode_number

import requests
import logging
from .consts import ROOT_SCREEN_PAYLOAD, HEADERS, SEARCH_PAYLOAD, MEDIA_PAYLOAD, SEASON_PAYLOAD, SCREEN_PAYLOAD, ROOT_SCREENS, HOME_SCREEN, COLLECTION_PAYLOAD, GRID_PAYLOAD
from typing import Any, Dict, List, Tuple, Union
from fuzzywuzzy import fuzz

# Logger
logger = logging.getLogger(__name__)


class GraphQL():

    # ================================================================
    #   __init__()
    # ================================================================
    def __init__(self, session: requests.Session, url: str, tag: str, metadata_language: str = 'fr'):
        self.session: requests.Session = session
        self.url: str = url
        self.tag: str = tag
        self.subscriptions: List[str] = []
        self.scopes: List[str] = []
        self.packages: List[str] = []
        if metadata_language.lower() == 'en' or metadata_language.lower() == 'english':
            self.metadata_language = 'ENGLISH'
        else:
            self.metadata_language = 'FRENCH'

    # ===================================================================
    #
    #   CATEGORIES
    #
    # ===================================================================

    # ================================================================
    #   get_root_categories()
    # ================================================================

    def get_root_categories(self) -> List[Category]:
        '''
        List home page categories
            Returns:
                List[Category]: A list of all categories.
        '''

        return self.get_elements_screen(id=None, root=True)

    # ================================================================
    #   get_elements()
    # ================================================================

    def get_elements(self, category: Category) -> List[Union[Category, ResultInfo]]:
        '''
        Returns category's elements
            Args:
                category (Category): The category
            Returns:
                List[Union[Category, ResultInfo]: A list of all the elements.
        '''
        if category is None:
            logger.error('No category provided')
            return None
        logger.debug(
            'Listing elements of category "{}"'.format(category.title))
        if category.type == 'screen':
            return self.get_elements_screen(category.id)
        elif category.type == 'rotator':
            return self.get_elements_rotator(category.id)
        elif category.type == 'grid':
            return self.get_elements_grid(category.id)

    # ================================================================
    #   get_elements_screen()
    # ================================================================

    def get_elements_screen(self, id: str, root: bool = False) -> List[Union[Category, ResultInfo]]:
        '''
        Returns screen category's elements
            Args:
                id (str): The screen ID
            Returns:
                List[Union[Category, ResultInfo]: A list of all the elements.
        '''
        if not root and (id is None or id.strip() == ''):
            logger.error('No ID provided')
            return None
        if root:
            logger.debug('Listing root elements')
        else:
            logger.debug('Listing elements of screen "{}"'.format(id))

        # Request
        # =========
        logger.debug('Making a GraphQL request')
        if root:
            payload = deepcopy(ROOT_SCREEN_PAYLOAD)
        else:
            payload = deepcopy(SCREEN_PAYLOAD)
            payload['variables']['id'] = id
        response = self._make_request(
            payload, playback_language=self.metadata_language)
        if response.status_code != 200:
            logger.error('Bad response received ({})'.format(
                response.status_code))
            return None

        # Parse
        # =======
        logger.debug('Parsing response...')
        elements = []

        # Screens
        # =========
        home_id = None
        try:
            if root:
                screens = json.loads(response.text)[
                    'data']['app']['navigationLinks']
            else:
                screens = json.loads(response.text)[
                    'data']['screen']['secondaryNavigation']['links']
            for screen in screens:
                try:
                    if root and screen['internalContent']['containerType'] == HOME_SCREEN:
                        home_id = screen['internalContent']['id']
                        continue
                    if root and not screen['internalContent']['containerType'] in ROOT_SCREENS:
                        continue
                    elements.append(Category(
                        type='screen', title=screen['linkLabel'], id=screen['internalContent']['id']))
                except:
                    logger.warn('Unable to parse one of the screens')
                    continue
        except:
            logger.error('Unable to parse screens response')

        # Collections
        # =============
        if root:
            if home_id is not None:
                elements += self.get_elements_screen(home_id)
            return elements
        try:
            collections = json.loads(response.text)[
                'data']['screen']['collections']
            if len(elements) == 0 and len(collections) == 1:
                if collections[0]['__typename'] == 'Grid':
                    return self.get_elements_grid(collections[0]['id'])
                elif collections[0]['__typename'] == 'Rotator':
                    return self.get_elements_rotator(collections[0]['id'])
                return None
            for collection in collections:
                try:
                    if not 'config' in collection or not collection['config']['displayTitle']:
                        continue
                    if collection['__typename'] == 'Rotator':
                        elements.append(
                            Category(type='rotator', title=collection['title'], id=collection['id']))
                    elif collection['__typename'] == 'Grid':
                        elements.append(
                            Category(type='grid', title=collection['title'], id=collection['id']))
                except:
                    logger.warn('Unable to parse one of the collections')
                    continue
        except:
            logger.error('Unable to parse collections response')
        return elements

    # ================================================================
    #   get_elements_grid()
    # ================================================================

    def get_elements_grid(self, id: str) -> List[Union[Category, ResultInfo]]:
        '''
        Returns grid category's elements
            Args:
                id (str): The grid ID
            Returns:
                List[Union[Category, ResultInfo]: A list of all the elements.
        '''
        if id is None or id.strip() == '':
            logger.error('No ID provided')
            return None
        logger.debug('Listing elements of collection "{}"'.format(id))

        # Request
        # =========
        payload = deepcopy(GRID_PAYLOAD)
        payload['variables']['id'] = id
        response = self._make_request(
            payload, playback_language=self.metadata_language)
        if response.status_code != 200:
            logger.error('Bad response received ({})'.format(
                response.status_code))
            return None

        # Parse
        # =======
        logger.debug('Parsing response...')
        elements = []
        try:
            items = json.loads(response.text)[
                'data']['grid']['collection']['page']['items']
            for item in items:
                try:
                    elements.append(self.parse_search_result(item))
                except:
                    continue
        except:
            logger.error('Unable to parse response')
            return None
        return elements

    # ================================================================
    #   get_elements_rotator()
    # ================================================================

    def get_elements_rotator(self, id: str) -> List[Union[Category, ResultInfo]]:
        '''
        Returns rotator category's elements
            Args:
                id (str): The rotator ID
            Returns:
                List[Union[Category, ResultInfo]: A list of all the elements.
        '''
        if id is None or id.strip() == '':
            logger.error('No ID provided')
            return None
        logger.debug('Listing elements of collection "{}"'.format(id))

        # Request
        # =========
        payload = deepcopy(COLLECTION_PAYLOAD)
        payload['variables']['id'] = id
        response = self._make_request(
            payload, playback_language=self.metadata_language)
        if response.status_code != 200:
            logger.error('Bad response received ({})'.format(
                response.status_code))
            return None

        # Parse
        # =======
        logger.debug('Parsing response...')
        elements = []
        try:
            items = json.loads(response.text)[
                'data']['rotator']['collection']['page']['items']
            for item in items:
                try:
                    elements.append(self.parse_search_result(item))
                except:
                    continue
        except:
            logger.error('Unable to parse response')
            return None
        return elements

    # ===================================================================
    #
    #   SEARCH
    #
    # ===================================================================

    # ================================================================
    #   search()
    # ================================================================

    def search(self, input: str) -> List[SearchResult]:
        '''
        Search a title.
            Args:
                input (str): The search terms
            Returns:
                List[SearchResult]: A list of all the search results. First element is the most relevent one.
        '''
        # Check arguments
        # =================
        if input is None or len(input.strip()) == 0:
            logger.info('No title provided')
            return []
        elif len(input.strip()) < 3:
            logger.info('Title must be at least 3 characters long')
            return []

        # Request
        # =========
        logger.debug('Making a GraphQL request...')
        payload = deepcopy(SEARCH_PAYLOAD)
        payload['variables']['searchTerm'] = input.strip()
        response = self._make_request(payload)
        if response.status_code != 200:
            logger.error('Bad response received ({})'.format(
                response.status_code))
            return None

        # Parse
        # =======
        logger.debug('Parsing response...')
        try:
            response_parsed = json.loads(response.text)
            response_parsed = response_parsed['data']['searchMedia']['page']['items']
            suggestions = []
            for item in response_parsed:
                result = self.parse_search_result(item)
                if result is None:
                    continue
                suggestions.append(
                    (fuzz.partial_ratio(result.title, input), result))
            logger.debug('Found {} matches'.format(str(len(suggestions))))
            return [x for _, x in sorted(suggestions, reverse=True)][:50]
        except:
            logger.error('An error occured while parsing response')
            return None

    # ================================================================
    #   parse_search_result()
    # ================================================================

    def parse_search_result(self, resp: Dict[str, Any]) -> SearchResult:
        try:
            result = SearchResult()
            result.title = resp['title']
            if len(resp['images']) > 0:
                result.image = resp['images'][0]['url']
            result.requirements = resp['resourceCodes']
            result.has_access = False
            for requirement in result.requirements:
                if requirement in self.scopes:
                    result.has_access = True
                    break
            result.platform_tag = self.tag
            result.search_title = result.title
            result.id = resp['id']
            return result
        except:
            return None

    # ===================================================================
    #
    #   RESULT INFOS
    #
    # ===================================================================

    # ================================================================
    #   get_result_infos()
    # ================================================================

    def get_result_infos(self, result: SearchResult) -> List[Union[MovieResultInfo, SerieResultInfo]]:
        '''
        Get more infos about a specific search result
            Args:
                result (SearchResult): The search result
            Returns:
                Dict[str, Union[MovieResultInfo, SerieResultInfo]]: A dictionary of all the versions available (french/english) and corresponding infos
        '''
        return self.get_result_infos_id(result.id)

    # ================================================================
    #   get_result_infos_id()
    # ================================================================

    def get_result_infos_id(self, content_id: str) -> List[Union[MovieResultInfo, SerieResultInfo]]:
        '''
        Get more infos about a specific search result
            Args:
                id (str): The result ID
            Returns:
                Dict[str, Union[MovieResultInfo, SerieResultInfo]]: A dictionary of all the versions available (french/english) and corresponding infos
        '''
        logger.debug('Getting infos for "{}"...'.format(content_id))

        # Check arguments
        # =================
        if content_id is None or len(content_id.strip()) == 0:
            logger.info('No Content ID provided')
            return []

        # Request
        # =========
        payload = deepcopy(MEDIA_PAYLOAD)
        payload['variables']['id'] = content_id
        responses = {}
        logger.debug('Making a GraphQL request for french version...')
        responses['fr'] = self._make_request(
            payload, playback_language='FRENCH')
        logger.debug('Making a GraphQL request for english version...')
        responses['en'] = self._make_request(
            payload, playback_language='ENGLISH')
        if responses['fr'].status_code != 200 and responses['en'].status_code != 200:
            logger.error('Bad responses ({}) ({})'.format(
                responses['fr'].status_code, responses['en'].status_code))
            return None

        # Parse
        # =======
        infos = {}
        logger.debug('Parsing responses...')
        for lang, response in responses.items():
            try:
                if response.status_code != 200:
                    logger.debug('Skipping {} version because of a bad response ()'.format(
                        response.status_code))
                    continue
                logger.debug('Parsing {} response...'.format(lang))
                response_parsed = json.loads(response.text)[
                    'data']['axisMedia']
                if response_parsed['mediaType'] == 'SERIES':
                    infos[lang] = self._parse_serie_result(
                        response_parsed, lang)
                elif response_parsed['mediaType'] == 'MOVIE':
                    infos[lang] = self._parse_movie_result(
                        response_parsed, lang)
            except:
                logger.error('Failed to parse {} response'.format(lang))
                infos.pop(lang, None)
                continue

        # Handle parsing error
        # ======================
        if len(infos) == 0:
            logger.error('Failed to parse all responses')
            return None

        # Manage versions
        # =================
        infos_formatted = {}
        for version, info in infos.items():
            if info is None or len(info.medias) == 0:
                continue
            info.version = version
            infos_formatted[version] = info
        logger.debug('Found {} versions ({})'.format(
            str(len(infos_formatted)), ', '.join(infos_formatted.keys())))
        return infos_formatted

    # ================================================================
    #   _parse_movie_result()
    # ================================================================

    def _parse_movie_result(self, result: Dict[str, Any], version: str) -> MovieResultInfo:
        '''
        Parses a movie response
            Args:
                result (Dict): The response as a Dict
                version (Dict): The targeted version (french or english)
            Returns:
                MovieResultInfo: The detailed movie infos
        '''
        infos = MovieResultInfo()
        infos.medias['default'] = MediaMovie()
        logger.debug(result)
        content = result['mainContents']['page']['items'][0]
        logger.debug(content)

        # Language check
        # ================
        for lang in content['axisPlaybackLanguages']:
            if lang['language'].lower() == version:
                infos.medias['default'].playback_languages.append(
                    lang['language'].lower())
                infos.medias['default'].additionnal_infos['destination'] = lang['destinationCode']
        if len(infos.medias['default'].playback_languages) == 0:
            logger.debug('Playback language does not fit request language')
            return None

        # Access check
        # ==============
        infos.medias['default'].has_access = False
        for constraint in content['authConstraints']:
            if constraint['language'].lower() == version:
                if constraint['packageName'] in self.packages:
                    infos.medias['default'].has_access = True
                    break

        # Movie infos
        # =============
        # Title
        infos.title = result['title']
        infos.medias['default'].title = result['title']
        # Image
        for image in result['images']:
            if image['format'] == 'POSTER':
                infos.image = image['url']
                infos.medias['default'].image = image['url']
                break
        # Summary
        infos.summary = result['summary']
        infos.medias['default'].summary = result['summary']
        # Description
        infos.description = result['description']
        infos.medias['default'].description = result['summary']

        # Play ID
        infos.medias['default'].play_id = str(content['axisId'])
        # Year
        try:
            date_str = content['broadcastDate']
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            infos.year = date.year
        except:
            pass
        # Duration
        try:
            duration_str = content['duration']
            duration = 0
            if 'h' in duration_str:
                index = duration_str.index('h')
                value = duration_str[:index]
                duration_str = duration_str[index+1:]
                duration += int(value.strip()) * 3600
            if 'm' in duration_str:
                index = duration_str.index('m')
                value = duration_str[:index]
                duration_str = duration_str[index+1:]
                duration += int(value.strip()) * 60
            if 's' in duration_str:
                index = duration_str.index('s')
                value = duration_str[:index]
                duration_str = duration_str[index+1:]
                duration += int(value.strip())
            infos.medias['default'].duration = duration
        except:
            pass
        return infos

    # ================================================================
    #   _parse_serie_result()
    # ================================================================

    def _parse_serie_result(self, result: Dict[str, Any], version: str) -> SerieResultInfo:
        '''
        Parses a serie response
            Args:
                result (Dict): The response as a Dict
                version (Dict): The targeted version (french or english)
            Returns:
                MovieResultInfo: The detailed serie infos
        '''
        # Show infos
        # ============
        infos = SerieResultInfo()
        # Title
        infos.title = result['title']
        # Image
        for image in result['images']:
            if image['format'] == 'POSTER':
                infos.image = image['url']
                break
        infos.title = result['title']
        # Summary
        infos.summary = result['summary']
        # Description
        infos.description = result['description']

        for season in result['seasons']:

            # Season metadata
            # =================
            try:
                season_num = int(season['seasonNumber'])
            except:
                logger.error('Unable to parse season number')
                continue

            # Season Request
            # ================
            payload = deepcopy(SEASON_PAYLOAD)
            payload['variables']['id'] = season['id']
            logger.debug('Making a GraphQL request for season {} ({})...'.format(
                str(season_num), version))
            langs = {'fr': 'FRENCH', 'en': 'ENGLISH'}
            response = self._make_request(
                payload, playback_language=langs[version])
            if response.status_code != 200:
                logger.error('Bad response ({})'.format(response.status_code))
                continue

            # Parse episodes
            # ================
            try:
                episodes = json.loads(response.text)[
                    'data']['axisSeason']['episodes']
            except:
                logger.error('Error while parsing response')
                continue
            for episode in episodes:

                # Episode metadata
                # ==================
                try:
                    episode_num = int(episode['episodeNumber'])
                    episode_tag = format_episode_number(
                        season_num, episode_num)
                except:
                    logger.error('Weird error while parsing an episode')
                    continue

                try:

                    # Episode language check
                    # ========================
                    dest_code = None
                    playback_languages = []
                    for lang in episode['axisPlaybackLanguages']:
                        if lang['language'].lower() == version:
                            dest_code = lang['destinationCode']
                            playback_languages.append(lang['language'].lower())
                    if dest_code == None:
                        logger.debug(
                            'Playback language does not fit request language ({})'.format(episode_tag))
                        continue

                    # Access check
                    # ==============
                    temp_episode = MediaEpisode()
                    temp_episode.has_access = False
                    for constraint in episode['authConstraints']:
                        if constraint['language'].lower() == version:
                            if constraint['packageName'] in self.packages:
                                temp_episode.has_access = True
                                break

                    # Episode infos
                    # ===============

                    # Episode
                    temp_episode.season = season_num
                    temp_episode.episode = episode_num
                    temp_episode.episode_tag = episode_tag
                    # Title
                    temp_episode.title = episode['title']
                    # Image
                    for image in episode['images']:
                        if image['format'] == 'THUMBNAIL':
                            temp_episode.image = image['url']
                            break
                    temp_episode.play_id = str(episode['axisId'])
                    # Summary
                    temp_episode.summary = episode['summary']
                    # Description
                    temp_episode.description = episode['description']
                    # Play ID
                    temp_episode.play_id = str(episode['axisId'])
                    # Duration
                    try:
                        duration_str = episode['duration']
                        duration = 0
                        if 'h' in duration_str:
                            index = duration_str.index('h')
                            value = duration_str[:index]
                            duration_str = duration_str[index+1:]
                            duration += int(value.strip()) * 3600
                        if 'm' in duration_str:
                            index = duration_str.index('m')
                            value = duration_str[:index]
                            duration_str = duration_str[index+1:]
                            duration += int(value.strip()) * 60
                        if 's' in duration_str:
                            index = duration_str.index('s')
                            value = duration_str[:index]
                            duration_str = duration_str[index+1:]
                            duration += int(value.strip())
                        temp_episode.duration = duration
                    except:
                        pass
                    # Playback Language
                    temp_episode.playback_languages = deepcopy(
                        playback_languages)
                    # Destination code
                    temp_episode.additionnal_infos['destination'] = dest_code
                    # Add episode
                    infos.medias[episode_tag] = temp_episode
                except:
                    logger.warn('Unable to parse version {} of {}'.format(
                        version, episode_tag))
                    continue
        return infos

    # ================================================================
    #   _make_request()
    # ================================================================

    def _make_request(self, partial_data: Dict[str, Any], playback_language: str = 'FRENCH') -> requests.Response:
        data = deepcopy(partial_data)
        data['variables']['subscriptions'] = self.subscriptions
        data['variables']['language'] = self.metadata_language
        data['variables']['playbackLanguage'] = playback_language
        return self.session.post(url=self.url, headers=HEADERS, json=data)
