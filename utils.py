import sys
from langs import get_text
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import os
import logging
import sys
from urllib.parse import parse_qs

LOGGER_INITIALIZED = False
ADDON = None
ADDON_NAME = None
PROFILE_DIR = None
CACHE_DIR = None
ADDON_DIR = None
RESOURCE_DIR = None
LOG_PATH = None
BASE_URL = None
URL = None
HANDLE = None
OBJ_TYPE = None
CMDS = None
SETTINGS = {}

LOGGER = logging.getLogger(__name__)


def get_addon():
    global ADDON
    if ADDON is None:
        ADDON = xbmcaddon.Addon()
    return ADDON


def get_addon_name():
    global ADDON_NAME
    if ADDON_NAME is None:
        ADDON_NAME = get_addon().getAddonInfo('name')
        LOGGER.debug('ADDON NAME: ' + str(ADDON_NAME))
    return ADDON_NAME


def get_profile_dir():
    global PROFILE_DIR
    if PROFILE_DIR is None:
        PROFILE_DIR = xbmcvfs.translatePath(
            get_addon().getAddonInfo('profile'))
        if not os.path.isdir(PROFILE_DIR):
            os.makedirs(PROFILE_DIR)
        LOGGER.debug('PROFILE DIR: ' + str(PROFILE_DIR))
    return PROFILE_DIR


def get_cache_dir():
    global CACHE_DIR
    if CACHE_DIR is None:
        CACHE_DIR = os.path.join(get_profile_dir(), 'cache')
        LOGGER.debug('CACHE DIR: ' + str(CACHE_DIR))
    return CACHE_DIR


def get_addon_dir():
    global ADDON_DIR
    if ADDON_DIR is None:
        ADDON_DIR = get_addon().getAddonInfo('path')
        LOGGER.debug('ADDON DIR: ' + str(ADDON_DIR))
    return ADDON_DIR


def get_ressource_dir():
    global RESOURCE_DIR
    if RESOURCE_DIR is None:
        RESOURCE_DIR = os.path.join(get_addon_dir(), 'resources')
        LOGGER.debug('RESOURCE DIR: ' + str(RESOURCE_DIR))
    return RESOURCE_DIR


def get_log_path():
    global LOG_PATH
    if LOG_PATH is None:
        LOG_PATH = os.path.join(get_profile_dir(), 'log.txt')
        LOGGER.debug('LOG PATH: ' + str(LOG_PATH))
    return LOG_PATH


def get_setting(setting_name):
    global SETTINGS
    if setting_name not in SETTINGS:
        SETTINGS[setting_name] = get_addon().getSetting(setting_name)
        LOGGER.debug('SETTING "' + str(setting_name) +
                     '": ' + str(SETTINGS[setting_name]))
    return SETTINGS[setting_name]


def check_user_pass():
    username = get_setting('username')
    password = get_setting('password')
    if username == None or username.strip() == '':
        xbmcgui.Dialog().ok(get_addon_name(), get_text('username_error'))
        exit(1)
    if password == None or password.strip() == '':
        xbmcgui.Dialog().ok(get_addon_name(), get_text('password_error'))
        exit(1)
    LOGGER.debug('Username and password format has been checked.')


def init_logger():
    global LOGGER_INITIALIZED
    if not LOGGER_INITIALIZED:
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] [%(module)s] %(message)s',
            datefmt='%Y-%m-%d,%H:%M:%S',
            filename=get_log_path())
        logging.getLogger().setLevel(logging.DEBUG)
        LOGGER.debug('Logger intialized.')
        LOGGER_INITIALIZED = True


def get_base_url():
    global BASE_URL
    if BASE_URL is None:
        BASE_URL = sys.argv[0]
        LOGGER.debug('BASE URL: ' + str(BASE_URL))
    return BASE_URL


def get_url():
    global URL
    if URL is None:
        URL = sys.argv[2]
        LOGGER.debug('URL: ' + str(URL))
    return URL


def get_handle():
    global HANDLE
    if HANDLE is None:
        HANDLE = int(sys.argv[1])
        LOGGER.debug('HANDLE: ' + str(HANDLE))
    return HANDLE


def get_obj_type():
    global OBJ_TYPE
    if OBJ_TYPE is None:
        parsed_url = parse_qs(get_url()[1:])
        OBJ_TYPE = parsed_url['obj_type'][0] if 'obj_type' in parsed_url else 'none'
        LOGGER.debug('OBJ TYPE: ' + str(OBJ_TYPE))
    return OBJ_TYPE


def get_cmds():
    global CMDS
    if CMDS is None:
        parsed_url = parse_qs(get_url()[1:])
        obj_type = get_obj_type()
        CMDS = 'none'
        if obj_type == 'none' and 'cmds' not in parsed_url:
            CMDS = 'main'
        if 'cmds' in parsed_url:
            CMDS = parsed_url['cmds'][0]
        LOGGER.debug('CMDS: ' + str(CMDS))
    return CMDS


def check_url():
    obj_type = get_obj_type()
    cmds = get_cmds()
    if obj_type not in ['category', 'result', 'media'] and cmds not in ['main', 'search']:
        LOGGER.error('No object or command provided.')
        exit(1)
    LOGGER.debug('Url format has been checked.')


def search_modal() -> str:
    searchStr = ''
    keyboard = xbmc.Keyboard(searchStr, 'Search')
    keyboard.doModal()
    if (keyboard.isConfirmed() == False):
        return None
    # .replace(' ','+')  # sometimes you need to replace spaces with + or %20
    searchStr = keyboard.getText()
    if len(searchStr) == 0:
        return
    else:
        return searchStr


init_logger()
