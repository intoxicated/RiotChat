""" 
User represents a user of lol player
"""
#from utils.misc import Division, Tier

class Status(object):
    def __init__(self, args=None):
        #self._level = kwargs['level']
        #self._wins =  kwargs['wins']
        #self._leaves = kwargs['leaves']
        #self._profIcon = kwargs['profile_icon']
        pass

class User(object):
    """





    """
    def __init__(self):
        pass


class Friend(User):

    def __init__(self, jid, name, substype, grpName):
        super(Friend, self).__init__()
        self._groupName = 'Default' if (grpName == '**Default') else grpName
        self._jid = jid
        self._name = name
        self._substype = substype
        self._status = Status()
        self._isOnline = False 

    @property
    def groupName(self):
        return self._groupName
    
    @groupName.setter
    def groupName(self, value):
        self._groupName = value

    @property
    def isOnline(self):
        return self._isOnline

    @isOnline.setter
    def isOnline(self, online):
        self._isOnline = online

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, kwargs):
        self._status = newstatus

    @property
    def jid(self):
        return self._jid

    @property 
    def name(self):
        return self._name



class Roster(object):
    def __init__(self):
        #key name : value (Friend object)
        self._grp = {}

    def add(self, summoner):
        if isinstance(summoner, Friend):
            self._grp[summoner.jid] = summoner
        else:
            raise Exception

    def remove(self, summoner):
        if summoner not in self.grp.keys():
            raise Exception
        else:
            del self._grp[summoner]

    def get(self, name):
        return self._grp[name]





