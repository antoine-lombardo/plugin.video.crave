from langs import get_text
from list_item_generator import add_item, add_search_item
from pycrave.common.category import Category
from pycrave.common.media import MediaEpisode
from pycrave.common.result_info import MovieResultInfo
from pycrave.common.search_result import SearchResult
from search import search_modal
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import ast
import sys
from urllib import parse
import inputstreamhelper

from list_item_generator import add_item

import os
import logging
from pycrave import Crave


PROTOCOL = 'mpd'
DRM = 'com.widevine.alpha'


# Logger
logger = logging.getLogger(__name__)

# Addon basics
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__addon_dir__ = xbmcvfs.translatePath(__addon__.getAddonInfo('profile'))

# Init addon dir
if not os.path.isdir(__addon_dir__):
    os.makedirs(__addon_dir__)

# Paths
cache_dir = os.path.join(__addon_dir__, 'cache')
log_path = os.path.join(__addon_dir__, 'log.txt')

# Logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] [%(module)s] %(message)s',
    datefmt='%Y-%m-%d,%H:%M:%S',
    filename=log_path)
logging.getLogger().setLevel(logging.DEBUG)

# Settings
username = __addon__.getSetting("username")
password = __addon__.getSetting("password")
metadata_lang = __addon__.getSetting("metadata_lang")
playback_lang = __addon__.getSetting("audio_lang")

if username == None or username.strip() == '':
    xbmcgui.Dialog().ok(__addonname__, get_text('username_error'))
    exit(1)

if password == None or password.strip() == '':
    xbmcgui.Dialog().ok(__addonname__, get_text('password_error'))
    exit(1)

crave = Crave(
    cache_dir=cache_dir,
    username=username,
    password=password,
    metadata_lang=metadata_lang
)

if crave.account_infos == None:
    xbmcgui.Dialog().ok(__addonname__, get_text('login_error'))
    exit(1)

# Requested path
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = parse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

view_modes = {
    'grid': '500',
    'thumb_right': '50',
    'list': '55',
    'caroussel': '51',
    'fixed_right': '502'
}
view_mode = view_modes['grid']

logger.debug(args)


if not 'obj_type' in args:
    # MAIN MENU
    if not 'cmds' in args:
        add_search_item()
        elements = crave.get_root_categories()
        if elements is not None:
            for element in elements:
                list_item = add_item(element, len(elements))
                if list_item is None:
                    continue
            xbmcplugin.endOfDirectory(addon_handle)
            xbmc.executebuiltin("Container.SetViewMode({})".format(view_mode))
    elif args['cmds'][0] == 'search':
        search_terms = search_modal()
        if search_terms is None or search_terms.strip() == '':
            exit(0)
        results = crave.search(search_terms)
        if results is not None:
            for result in results:
                if result.obj_type == 'result':
                    view_mode = view_modes['caroussel']
                list_item = add_item(result, len(results))
            xbmcplugin.endOfDirectory(addon_handle)
            xbmc.executebuiltin("Container.SetViewMode({})".format(view_mode))

# CATEGORY PROVIDED
elif args['obj_type'][0] == 'category':
    category = Category.from_args(args)
    elements = crave.get_elements(category)
    if elements is not None:
        for element in elements:
            if element.obj_type == 'result':
                view_mode = view_modes['caroussel']
            list_item = add_item(element, len(elements))
        xbmcplugin.endOfDirectory(addon_handle)
        xbmc.executebuiltin("Container.SetViewMode({})".format(view_mode))
# RESULT PROVIDED
elif args['obj_type'][0] == 'result':
    result = SearchResult.from_args(args)
    title = crave.get_result_infos(result)
    if title is not None and playback_lang in title:
        title = title[playback_lang]
        if title.type == 'serie':
            view_mode = view_modes['fixed_right']
        list_item = add_item(title)
        xbmcplugin.endOfDirectory(addon_handle)
        xbmc.executebuiltin("Container.SetViewMode({})".format(view_mode))
# MEDIA PROVIDED
elif args['obj_type'][0] == 'media':
    media = MediaEpisode.from_args(args)
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
