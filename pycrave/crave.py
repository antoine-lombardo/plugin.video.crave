# External stuff
from copy import copy
import json
import logging
from pycrave.common.category import Category

from pycrave.common.media import Media

# Common
from .common.play_infos import PlayInfos
from .common.result_info import ResultInfo
from .common.result_info import SerieResultInfo, MovieResultInfo
from .common.search_result import SearchResult
from .common.account import Account
from .common.platform import Platform
from .common.utils import format_episode_number

# Crave stuff
from .login_handler import CraveLoginHandler
from .consts import *
from typing import Any, Dict, List, Union

# Internal libs
from .lib.graphql.graphql import GraphQL
from .lib.capi.capi import CAPI

# Logger
logger = logging.getLogger(__name__)


class Crave(Platform):
    name = 'Crave'
    tag = 'crave'

    # ================================================================
    #   __init__()
    # ================================================================

    def __init__(self, cache_dir: str, username: str = None, password: str = None, metadata_lang: str = 'fr'):
        '''
        Initialises the client.
            Args:
                cache_dir (str): Directory to store cache files
                username (str): Account username
                password (str): Account password
                metadata_lang (str): Language used to fetch metadata
        '''
        super().__init__(cache_dir)
        self.graphql = GraphQL(self.session, 'https://www.crave.ca/space-graphql/graphql/',
                               self.tag, metadata_language=metadata_lang)
        self.login_handler: CraveLoginHandler = CraveLoginHandler(
            self.cache_dir, self.session, username, password)
        self.account_infos: Account = None
        if self.login_handler.ensure_login():
            self.get_account_infos()
        else:
            logger.info('Unable to login')

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
        logger.debug('Listing root categories...')
        return self.graphql.get_root_categories()

    # ================================================================
    #   get_elements()
    # ================================================================

    def get_elements(self, category: Category) -> List[Union[Category, ResultInfo]]:
        '''
        List all category elements
            Returns:
                List[Union[Category, ResultInfo]]: A list of elements in category
        '''
        return self.graphql.get_elements(category)

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
        logger.debug('Making a search for "{}"...'.format(input))
        return self.graphql.search(input)

    # ===================================================================
    #
    #   RESULT INFOS
    #
    # ===================================================================

    # ================================================================
    #   get_result_infos()
    # ================================================================

    def get_result_infos(self, result: SearchResult) -> Dict[str, Union[MovieResultInfo, SerieResultInfo]]:
        '''
        Get more infos about a specific search result
            Args:
                result (SearchResult): The search result
            Returns:
                Dict[str, Union[MovieResultInfo, SerieResultInfo]]: A dictionary of all the versions available (french/english) and corresponding infos
        '''
        logger.debug('Getting infos for "{}"...'.format(result.title))
        return self.graphql.get_result_infos(result)

    # ================================================================
    #   get_result_infos_id()
    # ================================================================

    def get_result_infos_id(self, content_id: str) -> Dict[str, Union[MovieResultInfo, SerieResultInfo]]:
        '''
        Get more infos about a specific search result
            Args:
                id (str): The Content ID
            Returns:
                Dict[str, Union[MovieResultInfo, SerieResultInfo]]: A dictionary of all the versions available (french/english) and corresponding infos
        '''
        logger.debug('Getting infos for "{}"...'.format(content_id))
        return self.graphql.get_result_infos_id(content_id)

    # ===================================================================
    #
    #   PLAY INFOS
    #
    # ===================================================================

    # ================================================================
    #   get_play_infos()
    # ================================================================

    def get_play_infos(self, result_infos: ResultInfo, season: int = None, episode: int = None) -> PlayInfos:
        '''
        Returns play infos for the provided result infos
            Args:
                result_infos (ResultInfo): The result infos
                season (int): The season number (only for series)
                episode (int): The episode number (only for series)
            Returns:
                PlayInfos: The play infos
        '''
        if result_infos.type == 'movie':
            return self._get_play_infos_movie(result_infos)
        elif result_infos.type == 'serie':
            return self._get_play_infos_episode(result_infos, season, episode)
        return None

    # ================================================================
    #   _get_play_infos_movie()
    # ================================================================

    def _get_play_infos_movie(self, result_infos: MovieResultInfo) -> PlayInfos:
        '''
        Returns play infos for the provided movie
            Args:
                result_infos (ResultInfo): The movie
            Returns:
                PlayInfos: The play infos
        '''
        if result_infos.year > 0:
            logger.debug('Getting play infos for "{} ({})"...'.format(
                result_infos.title, str(result_infos.year)))
        else:
            logger.debug('Getting play infos for "{}"...'.format(
                result_infos.title))
        return self._get_play_infos_media(result_infos.medias['default'])

    # ================================================================
    #   _get_play_infos_episode()
    # ================================================================

    def _get_play_infos_episode(self, result_infos: SerieResultInfo, season: int, episode: int) -> PlayInfos:
        '''
        Returns play infos for the provided serie episode
            Args:
                result_infos (ResultInfo): The serie
                season (int): The season number
                episode (int): The episode number
            Returns:
                PlayInfos: The play infos
        '''
        if season is None or episode is None:
            logger.error('No season or episode provided')
            return None
        logger.debug('Getting play infos for "{} {}"...'.format(
            result_infos.title, format_episode_number(season, episode)))
        for media in result_infos.medias.values():
            if media.season == season and media.episode == episode:
                return self._get_play_infos_media(media)
        logger.debug('Episode {} not found'.format(
            format_episode_number(season, episode)))

    # ================================================================
    #   _get_play_infos_media()
    # ================================================================

    def _get_play_infos_media(self, media: Media) -> PlayInfos:
        '''
        Returns play infos for the provided media
            Args:
                media (Media): The media
            Returns:
                PlayInfos: The play infos
        '''
        if not media.has_access:
            logger.error('You don\'t have access to this content')
            return None
        return self._get_play_infos_id(
            id=media.play_id,
            destination=media.additionnal_infos['destination'],
            language=media.playback_languages[0])

    # ================================================================
    #   _get_play_infos_id()
    # ================================================================

    def _get_play_infos_id(self, id: str, destination: str, language: str = 'fr') -> PlayInfos:
        '''
        Returns play infos for the provided media ID
            Args:
                id (str): The media ID
                destination (str): The destination ID
                language (str): The language ('fr' or 'en')
            Returns:
                PlayInfos: The play infos
        '''
        if not self.ensure_login():
            return None
        return CAPI.get_play_infos(destination, id, language, token=self.login_handler.access_token, filter='0x14')

    # ===================================================================
    #
    #   ACCOUNT
    #
    # ===================================================================

    # ================================================================
    #   login()
    # ================================================================

    def login(self, username: str, password: str) -> bool:
        self.account_infos = None
        if not self.login_handler.login(username, password):
            return False
        if self.get_account_infos() is None:
            return False
        return True

    # ================================================================
    #   logout()
    # ================================================================

    def logout(self) -> None:
        self.account_infos = None
        self.login_handler.logout()

    # ================================================================
    #   ensure_login()
    # ================================================================

    def ensure_login(self) -> bool:
        return self.login_handler.ensure_login()

    # ================================================================
    #   get_account_infos()
    # ================================================================

    def get_account_infos(self) -> Account:
        if not self.login_handler.ensure_login():
            self.account_infos = None
            return None
        try:
            self.graphql.subscriptions = self.login_handler.subscriptions
            self.graphql.scopes = self.login_handler.scopes
            self.graphql.packages = self.login_handler.packages
            self.account_infos = Account()
            url = 'https://account.bellmedia.ca/api/profile/v1.1'
            response = self._make_request_bearer(url=url, method='GET')
            response_parsed = json.loads(response.text)
            self.account_infos.name = response_parsed[0]['nickname']
            self.account_infos.picture = response_parsed[0]['avatarUrl']
            return self.account_infos
        except:
            self.account_infos = None
            return None

    # ===================================================================
    #   REQUESTS
    # ===================================================================

    # ================================================================
    #   _make_request_license()
    # ================================================================

    def _make_request_license(self, url: str, token: str, challenge):
        headers = copy(BASE_HEADERS)
        headers['Authorization'] = 'Bearer ' + token
        return self._make_request(url, headers=headers, data=challenge, method='POST-DATA').content

    # ================================================================
    #   _make_request_bearer()
    # ================================================================

    def _make_request_bearer(self, url: str, data: Dict[str, Any] = {}, method: str = 'POST'):
        if not self.login_handler.ensure_login():
            return None
        headers = copy(BASE_HEADERS)
        headers['Authorization'] = 'Bearer ' + self.login_handler.access_token
        return self._make_request(url, headers=headers, data=data, method=method)
