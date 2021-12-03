import utils
from pycrave import Crave
import logging
import os
import inputstreamhelper
from urllib import parse
import sys
import ast
import xbmcvfs
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmc
from pycrave.common.search_result import SearchResult
from pycrave.common.result_info import MovieResultInfo
from pycrave.common.media import Media, MediaEpisode
from pycrave.common.category import Category
from list_items import add_item, add_search_item
from langs import get_text


PROTOCOL = 'mpd'
DRM = 'com.widevine.alpha'


# LOGGER
LOGGER = logging.getLogger(__name__)


# VARIABLES
ADDON = utils.get_addon()
ADDON_NAME = utils.get_addon_name()
CACHE_DIR = utils.get_cache_dir()

# SETTINGS
USERNAME = utils.get_setting('username')
PASSWORD = utils.get_setting('password')
META_LANG = utils.get_setting('metadata_lang')
PLAY_LANG = utils.get_setting('audio_lang')
utils.check_user_pass()

# PARSE ARGUMENTS
BASE_URL = utils.get_base_url()
ADDON_HANDLE = utils.get_handle()
URL = utils.get_url()
OBJ_TYPE = utils.get_obj_type()
CMDS = utils.get_cmds()
utils.check_url()

# INITIALIZE CLIENT
crave = Crave(
    cache_dir=CACHE_DIR,
    username=USERNAME,
    password=PASSWORD,
    metadata_lang=META_LANG
)

# CHECK LOGIN
if crave.account_infos == None:
    xbmcgui.Dialog().ok(ADDON_NAME, get_text('login_error'))
    exit(1)

# SETUP GUI
xbmcplugin.setContent(ADDON_HANDLE, 'movies')
view_modes = {
    'grid': '500',
    'thumb_right': '50',
    'list': '55',
    'caroussel': '51',
    'fixed_right': '502'
}
view_mode = view_modes['grid']

# COMMAND
if OBJ_TYPE == 'none':

    # COMMAND: MAIN MENU
    if CMDS == 'main':
        add_search_item()
        elements = crave.get_root_categories()
        if elements is not None:
            for element in elements:
                list_item = add_item(element, len(elements))
                if list_item is None:
                    continue
            xbmcplugin.endOfDirectory(ADDON_HANDLE)
            xbmc.executebuiltin("Container.SetViewMode({})".format(view_mode))

    # COMMAND: SEARCH
    elif CMDS == 'search':
        search_terms = utils.search_modal()
        if search_terms is None or search_terms.strip() == '':
            exit(0)
        results = crave.search(search_terms)
        if results is not None:
            for result in results:
                if result.obj_type == 'result':
                    view_mode = view_modes['caroussel']
                list_item = add_item(result, len(results))
            xbmcplugin.endOfDirectory(ADDON_HANDLE)
            xbmc.executebuiltin("Container.SetViewMode({})".format(view_mode))

# CATEGORY PROVIDED
elif OBJ_TYPE == 'category':
    category = Category.from_url(URL)
    elements = crave.get_elements(category)
    if elements is not None:
        for element in elements:
            if element.obj_type == 'result':
                view_mode = view_modes['caroussel']
            list_item = add_item(element, len(elements))
        xbmcplugin.endOfDirectory(ADDON_HANDLE)
        xbmc.executebuiltin("Container.SetViewMode({})".format(view_mode))

# RESULT PROVIDED
elif OBJ_TYPE == 'result':
    result = SearchResult.from_url(URL)
    title = crave.get_result_infos(result)
    if title is not None and PLAY_LANG in title:
        title = title[PLAY_LANG]
        if title.type == 'serie':
            view_mode = view_modes['fixed_right']
        list_item = add_item(title)
        xbmcplugin.endOfDirectory(ADDON_HANDLE)
        xbmc.executebuiltin("Container.SetViewMode({})".format(view_mode))

# MEDIA PROVIDED
elif OBJ_TYPE == 'media':
    media = Media.from_url(URL)
    play_infos = crave._get_play_infos_media(media)

    is_helper = inputstreamhelper.Helper(PROTOCOL, drm=DRM)
    if is_helper.check_inputstream():
        play_item = xbmcgui.ListItem(path=play_infos.manifest_url)
        play_item.setProperty(
            'inputstream', is_helper.inputstream_addon)
        play_item.setProperty(
            'inputstream.adaptive.manifest_type', PROTOCOL)
        play_item.setProperty('inputstream.adaptive.license_type', DRM)
        play_item.setProperty(
            'inputstream.adaptive.license_key', play_infos.license_url + '||R{SSM}|')
        player = xbmc.Player()
        player.play(item=play_infos.manifest_url, listitem=play_item)
