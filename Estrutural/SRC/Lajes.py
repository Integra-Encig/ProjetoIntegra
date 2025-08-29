
from SCR.abstract.Slabs import *

class Lajes(Slabs):

    def __init__(self, object):
        self.id = object.id()
    
    @property
    def _id(self):
        return self.id
    @_id.setter
    def _id(self, object):
        self.id = object
    