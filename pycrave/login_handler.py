import json, logging
from typing import Dict, List
from datetime import datetime, timedelta
import base64

from .common.login_handler import LoginHandler
from .consts import *

# Logger
logger = logging.getLogger(__name__)

class CraveLoginHandler(LoginHandler):
  access_token: str = None
  refresh_token: str = None
  expiry: datetime = None

  scopes: List[str] = None
  subscriptions: List[str] = None
  packages: List[str] = None

  def __init__(self, cache_dir, session, username=None, password=None):
    super().__init__(cache_dir, session, username, password)
    if self.username is None or self.password is None:
      self._load_cache()
    else:
      self._load_cache()
      if self.username != username or self.password != password:
        self.access_token = None
        self.refresh_token = None
        self.expiry = None
        self.subscriptions = None
        self.scopes = None
        self.packages = None
        self.username = username
        self.password = password
        self._save_cache()
    self.ensure_login(False)

  # ===================================================================
  #   LOGIN
  # ===================================================================

  def login(self, username: str, password: str) -> bool:
    logger.debug('Logging in...')
    # Set username and password
    self.username = username
    self.password = password
    self.access_token = None
    self.refresh_token = None
    self.expiry = None
    self.subscriptions = None
    # Make login
    return self.ensure_login()

  def logout(self) -> None:
    logger.debug('Logging out...')
    self.username = None
    self.password = None
    self.access_token = None
    self.refresh_token = None
    self.expiry = None
    self.subscriptions = None
    self._save_cache()

  def ensure_login(self, force_refresh: bool = False) -> bool:
    #===========================================================
    # Check credentials
    #===========================================================
    if self.username is None or self.password is None:
      self.access_token = None
      self.refresh_token = None
      self.expiry = None
      self.subscriptions = None
      self._save_cache()
      logger.info('Cannot ensure logging: No username or password provided')
      return False

    #===========================================================
    # Skip if current token is valid
    #===========================================================
    if not self._check_expiry() and not force_refresh:
      return True

    #===========================================================
    # Refresh token if possible
    #===========================================================
    logger.debug('Refreshing token...')
    response = None
    if self.refresh_token is not None:
      response = self._make_refresh_request()
      if response.status_code != 200:
        logger.debug('Refreshing token failed')
        response = None

    #===========================================================
    # Do a username/password login if required
    #===========================================================
    if response is None:
      logger.debug('Trying username/password login...')
      response = self._make_login_request()

    #===========================================================
    # Handle refresh + login failure
    #===========================================================
    if response.status_code != 200:
      logger.info('Login failed')
      # Reset attributes
      self.access_token = None
      self.refresh_token = None
      self.expiry = None
      self.subscriptions = None
      self._save_cache()
      return False

    #===========================================================
    # Parse refresh/login response
    #===========================================================
    try:
      response_parsed = json.loads(response.text)
      self.access_token = response_parsed['access_token']
      self.refresh_token = response_parsed['refresh_token']
      self.expiry = datetime.now() + timedelta(0,response_parsed['expires_in'])
      # Scopes
      scopes = response_parsed['scope'].split(' ')
      for scope in scopes:
        if scope.startswith('subscription:'):
          self.scopes = scope.replace('subscription:', '').split(',')
      # Subscriptions
      self.subscriptions = []
      for scope in self.scopes:
        if scope in SCOPE_TO_SUBSCRIPTION_NAME:
          self.subscriptions.append(SCOPE_TO_SUBSCRIPTION_NAME[scope])
      # Packages
      self.packages = []
      for subscription in self.subscriptions:
        if subscription in SUBSCRIPTION_NAME_TO_PACKAGE_NAME:
          self.packages.append(SUBSCRIPTION_NAME_TO_PACKAGE_NAME[subscription])
      self._save_cache()
      logger.debug('New token acquired. Valid until: {}'.format(self.expiry.strftime("%Y/%m/%d %H:%M:%S")))
      return True
    except:
      #===========================================================
      # Handle invalid refresh/login response
      #===========================================================
      logger.info('Refresh/login response invalid')
      self.access_token = None
      self.refresh_token = None
      self.expiry = None
      self.subscriptions = None
      self._save_cache()
      return False

  # ===================================================================
  #   REQUESTS
  # ===================================================================

  def _make_refresh_request(self):
    logger.debug('Making a refresh request...')
    url = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=refresh_token'
    headers = {
      'accept-encoding': 'gzip',
      'authorization': 'Basic {}'.format(self._get_authorization()),
      'connection': 'Keep-Alive',
      'content-type': 'application/x-www-form-urlencoded',
      'user-agent': 'okhttp/4.9.0'
    }
    data = 'refresh_token={}'.format(self.refresh_token)
    return self.session.post(url=url, headers=headers, data=data)

  def _make_login_request(self):
    print('logging in user username and password...')
    url = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=password'
    headers = {
      'accept-encoding': 'gzip',
      'authorization': 'Basic {}'.format(self._get_authorization()),
      'connection': 'Keep-Alive',
      'content-type': 'application/x-www-form-urlencoded',
      'user-agent': 'okhttp/4.9.0'
    }
    data = 'password={}&username={}'.format(self.password, self.username)
    return self.session.post(url=url, headers=headers, data=data)

  def _get_authorization(self) -> str:
    decoded = '{}:{}'.format(CLIENT_ID, CLIENT_PASS)
    encoded = decoded.encode()
    b64 = base64.b64encode(encoded)
    return b64.decode()

  # ===================================================================
  #   TOKEN EXPIRY HANDLER
  # ===================================================================

  def _check_expiry(self) -> bool:
    # Check if credentials are provided
    if self.expiry is None or self.access_token is None or self.refresh_token is None:
      return True
    if self.expiry < datetime.now() - timedelta(0, 3600):
      return True
    return False

  # ===================================================================
  #   OVERLOADS
  # ===================================================================

  def _process_cache_obj(self, cache_obj) -> bool:
    if cache_obj is not None:
      try:
        self.username = cache_obj['username']
        self.password = cache_obj['password']
        self.access_token = cache_obj['access_token']
        self.refresh_token = cache_obj['refresh_token']
        self.subscriptions = cache_obj['subscriptions']
        self.scopes = cache_obj['scopes']
        self.packages = cache_obj['packages']
        try:
          self.expiry = datetime.strptime(cache_obj['expiry'], '%Y/%m/%d %H:%M:%S')
        except:
          self.expiry = None
        return True
      except:
        pass
      self.username = None
      self.password = None
      self.access_token = None
      self.refresh_token = None
      self.expiry = None
      self.subscriptions = None
      self.scopes = None
      self.packages = None
      return False

  def _create_cache_obj(self) -> Dict[str, str]:
    try:
      expiry = self.expiry.strftime("%Y/%m/%d %H:%M:%S")
    except:
      expiry = None
    return  {
      'username': self.username,
      'password': self.password,
      'access_token': self.access_token,
      'refresh_token': self.refresh_token,
      'expiry': expiry,
      'subscriptions': self.subscriptions,
      'scopes': self.scopes,
      'packages': self.packages
    }