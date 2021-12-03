import xbmcaddon

ADDON = xbmcaddon.Addon()
META_LANG = ADDON.getSetting("metadata_lang")

DICT = {
    'username_error': {
        'fr': "Nom d'utilisateur non défini",
        'en': 'No username provided'
    },
    'password_error': {
        'fr': 'Mot de passe non défini',
        'en': 'No password provided'
    },
    'login_error': {
        'fr': 'Impossible de se connecter',
        'en': 'Unable to login'
    }
}


def get_text(id: str) -> str:
    if id not in DICT:
        return ''
    if metadata_lang not in DICT[id]:
        return ''
    return DICT[id][metadata_lang]
