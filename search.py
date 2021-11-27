import xbmc


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
