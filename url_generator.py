import sys
from urllib.parse import urlencode

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])


def url_generator(query):
    return base_url + '?' + urlencode(query)
