import os
from . import settings
class User:
    def __init__(self,name):
        self.name = name
        self.home = os.path.join(settings.home_path,name)

