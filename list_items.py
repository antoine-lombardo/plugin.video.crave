import xbmcgui
import xbmcplugin
import xbmcaddon
import sys
import os
import utils
import logging
from urllib.parse import urlencode
from pycrave.common.media import Media

# LOGGER
LOGGER = logging.getLogger(__name__)

# VARIABLES
BASE_URL = utils.get_base_url()
ADDON_HANDLE = utils.get_handle()
RESOURCE_DIR = utils.get_ressource_dir()


def add_search_item():
    list_item = xbmcgui.ListItem('Search')
    list_item.setArt({'thumb': os.path.join(RESOURCE_DIR, 'search.png')})
    xbmcplugin.addDirectoryItem(
        handle=ADDON_HANDLE, url=BASE_URL + '?' + urlencode({'cmds': 'search'}), listitem=list_item, isFolder=True)


def add_item(element, total=None):
    if element.obj_type == 'category':
        return add_item_category(element, total)
    elif element.obj_type == 'result':
        return add_item_result(element, total)
    elif element.obj_type == 'title':
        return add_item_title(element)


def add_item_category(element, total):
    list_item = xbmcgui.ListItem(element.title)
    list_item.setArt({'thumb': os.path.join(RESOURCE_DIR, 'folder.png')})
    if total is None:
        xbmcplugin.addDirectoryItem(
            handle=ADDON_HANDLE, url=element.to_url(BASE_URL), listitem=list_item, isFolder=True)
    else:
        xbmcplugin.addDirectoryItem(
            handle=ADDON_HANDLE, url=element.to_url(BASE_URL), listitem=list_item, isFolder=True, totalItems=total)


def add_item_result(element, total):
    list_item = xbmcgui.ListItem(element.title)
    if element.image != '':
        list_item.setArt({'thumb': element.image})
    list_item.setInfo(
        'video', {'title': element.title})
    if total is None:
        xbmcplugin.addDirectoryItem(
            handle=ADDON_HANDLE, url=element.to_url(BASE_URL), listitem=list_item, isFolder=True)
    else:
        xbmcplugin.addDirectoryItem(
            handle=ADDON_HANDLE, url=element.to_url(BASE_URL), listitem=list_item, isFolder=True, totalItems=total)


def add_item_title(element):
    if element.type == 'serie':
        return add_item_title_serie(element)
    elif element.type == 'movie':
        add_item_title_movie(element)


def add_item_title_serie(element):
    for episode_tag in sorted(element.medias, reverse=True):
        media = element.medias[episode_tag]
        list_item = xbmcgui.ListItem(episode_tag)
        if media.image != '':
            list_item.setArt({'thumb': media.image,
                              'poster': media.image,
                              'banner': media.image,
                              'fanart': media.image,
                              'clearart': media.image,
                              'clearlogo': media.image,
                              'landscape': media.image,
                              'icon': media.image,
                              })
        infos = {'title': media.title, 'plot': media.description, 'episode': media.episode,
                 'season': media.season, 'duration': media.duration, 'tvshowtitle': element.title}
        list_item.setInfo(
            'video', infos)
        xbmcplugin.addDirectoryItem(
            handle=ADDON_HANDLE, url=media.to_url(BASE_URL), listitem=list_item, isFolder=False)


def add_item_title_movie(element):
    media = element.medias['default']
    LOGGER.debug(media)
    list_item = xbmcgui.ListItem(element.title)
    if media.image != '':
        list_item.setArt({'thumb': media.image,
                          'poster': media.image,
                          'banner': media.image,
                          'fanart': media.image,
                          'clearart': media.image,
                          'clearlogo': media.image,
                          'landscape': media.image,
                          'icon': media.image,
                          })
    infos = {'title': element.title, 'plot': media.description, 'year': element.year,
             'duration': media.duration}
    list_item.setInfo(
        'video', infos)
    xbmcplugin.addDirectoryItem(
        handle=ADDON_HANDLE, url=media.to_url(BASE_URL), listitem=list_item, isFolder=False)
