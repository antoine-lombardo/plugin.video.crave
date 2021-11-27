# ===================================================================
#
#   LOGIN HANDLER CONFIG
#
# ===================================================================

CLIENT_ID = "crave-android"
CLIENT_PASS = 'default'





# ===================================================================
#
#   GRAPHQL CONFIG
#
# ===================================================================

GRAPHQL_URL = 'https://www.crave.ca/space-graphql/graphql/'





# ===================================================================
#
#   SUBSCRIPTIONS CONFIG
#
# ===================================================================

DESTINATION_TO_SUBSCRIPTION = {
  'starz_atexace': 'starz',
  'crave_atexace': 'crave',
  'se_atexace':    'superecran'
}

SUBSCRIPTION_NAME_TO_PACKAGE_NAME = {
  'STARZ':       'starz_atexace',
  'CRAVE':       'crave_atexace',
  'SUPER_ECRAN': 'se_atexace'
}

SCOPE_TO_SUBSCRIPTION_NAME = {
  'crave_total': 'CRAVE_TOTAL',
  'cravep':      'CRAVE_PLUS',
  'cravetv':     'CRAVE',
  'se':          'SUPER_ECRAN',
  'starz':       'STARZ'
}





# ===================================================================
#
#   HEADERS
#
# ===================================================================

BASE_HEADERS = {
  'accept-encoding': 'gzip',
  'connection': 'Keep-Alive',
  'user-agent': 'okhttp/4.9.0'
}

CAPI_HEADERS = {
  'accept-encoding': 'identity',
  'connection': 'Keep-Alive',
  'user-agent': 'okhttp/4.9.0'
}

HEADERS = {
  'accept': 'application/json',
  'accept-encoding': 'gzip',
  'connection': 'Keep-Alive',
  'content-type': 'application/json; charset=utf-8',
  'graphql-client-platform': 'entpay_android',
  'user-agent': 'okhttp/4.9.0'
}