from typing import List


class Account():
  def __init__(self):
    self.name: str = ''
    self.picture: str = ''
    self.capabilities: List[str] = []

  def to_dict(self):
    return {
      'name': self.name,
      'picture': self.picture,
      'capabilities': self.capabilities
    }
