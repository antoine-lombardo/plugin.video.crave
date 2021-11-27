import os, requests, pickle
from typing import Dict
from abc import ABC, abstractmethod

class LoginHandler(ABC):
  cache_file: str
  session: requests.Session
  username: str
  password: str

  def __init__(self, cache_dir: str, session: requests.Session, username=None, password=None) -> None:
    self.cache_file = os.path.join(cache_dir, 'login.pck')
    self.session = session
    self.username = username
    self.password = password

  def _load_cache(self) -> bool:
    login_infos = None
    if os.path.isfile(self.cache_file):
      try:
        with open(self.cache_file, 'rb') as file:
          login_infos = pickle.load(file)
      except:
        os.remove(self.cache_file)
    return self._process_cache_obj(login_infos)

  def _save_cache(self) -> bool:
    if self.username is None or self.password is None:
      return False
    login_infos = self._create_cache_obj()
    if os.path.isfile(self.cache_file):
      os.remove(self.cache_file)
    with open(self.cache_file, 'wb') as file:
      pickle.dump(login_infos, file)
    return True

  def _process_cache_obj(self, cache_obj) -> bool:
    if cache_obj is None:
      self.username = None
      self.password = None
      return False
    else:
      self.username = cache_obj['username']
      self.password = cache_obj['password']
      return True

  def _create_cache_obj(self) -> Dict[str, str]:
    return  {
      'username': self.username,
      'password': self.password
    }
