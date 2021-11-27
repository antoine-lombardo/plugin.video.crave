import xbmcgui
import xbmcplugin
import xbmcaddon
import sys
import os
import urllib.parse
import logging
from url_generator import url_generator

# Logger
logger = logging.getLogger(__name__)

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urllib.parse.parse_qs(sys.argv[2][1:])
__addon__ = xbmcaddon.Addon()
__addonpath__ = __addon__.getAddonInfo('path')
__resourcepath__ = os.path.join(__addonpath__, 'resources')


def add_search_item():
    list_item = xbmcgui.ListItem('Search')
    list_item.setArt({'thumb': os.path.join(__resourcepath__, 'search.png')})
    xbmcplugin.addDirectoryItem(
        handle=addon_handle, url=url_generator({'cmds': 'search'}), listitem=list_item, isFolder=True)


def add_item(element, total=None):
    if element.obj_type == 'category':
        return add_item_category(element, total)
    elif element.obj_type == 'result':
        return add_item_result(element, total)
    elif element.obj_type == 'title':
        return add_item_title(element)


def add_item_category(element, total):
    list_item = xbmcgui.ListItem(element.title)
    list_item.setArt({'thumb': os.path.join(__resourcepath__, 'folder.png')})
    if total is None:
        xbmcplugin.addDirectoryItem(
            handle=addon_handle, url=url_generator(element.to_dict()), listitem=list_item, isFolder=True)
    else:
        xbmcplugin.addDirectoryItem(
            handle=addon_handle, url=url_generator(element.to_dict()), listitem=list_item, isFolder=True, totalItems=total)


def add_item_result(element, total):
    list_item = xbmcgui.ListItem(element.title)
    if element.image != '':
        list_item.setArt({'thumb': element.image})
    list_item.setInfo(
        'video', {'title': element.title})
    if total is None:
        xbmcplugin.addDirectoryItem(
            handle=addon_handle, url=url_generator(element.to_dict()), listitem=list_item, isFolder=True)
    else:
        xbmcplugin.addDirectoryItem(
            handle=addon_handle, url=url_generator(element.to_dict()), listitem=list_item, isFolder=True, totalItems=total)


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
            handle=addon_handle, url=url_generator(media.to_dict()), listitem=list_item, isFolder=False)


def add_item_title_movie(element):
    pass
