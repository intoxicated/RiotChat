""" 
User represents a user of lol player
"""
#from utils.misc import Division, Tier

from models.riot_exception import *

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
        self._status = {} # Status()
        self._isOnline = False 
    
    def get_status(self):
        formatStr = ""
        
        for k,v in self._status.items():
            formatStr += "{:<10} {:<10}".format(k,v)
        return formatStr

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
    def status(self, status):
        self._status = status

    @property
    def jid(self):
        return self._jid

    @property 
    def name(self):
        return self._name

class RosterManager(object):
    def __init__(self):
        #key name : value (Friend object)
        self._offlineGrp = {}
        self._onlineGrp = {}

    def add(self, summoner, online=False):
        if not isinstance(summoner, Friend):
            raise Exception
        if not isOnline:
            self._offlineGrp[summoner.jid] = summoner
        else: 
            self._onlineGrp[summoner.jid] = summoner

    def updateStatus(self, jid, status, online=False):
        fentry = "" #dummy
        if online:
            #if originally offline
            if self._offlineGrp.get(jid) != None:
                #get entry from offline
                fentry = self._offlineGrp[jid]
                #remove from offline
                del self._offlineGrp[jid]
            else:
                fentry = self._onlineGrp[jid]
            #update status
            fentry.status = status
            #insert into online
            self._onlineGrp[jid] = fentry

        else:
            #offline case, just remove status
            fentry = self._onlineGrp[jid]
            del self._onlineGrp[jid]

            fentry.status = {} # empty dict
            self._offlineGrp[jid] = fentry

    def remove(self, jid):
        """ unsubscribe a friend """
        if self._onlineGrp.get(jid) != None:
            del self._onlineGrp[jid]
        elif self._offlineGrp.get(jid) != None:
            del self._offlineGrp[jid]
        else:
            raise Exception

    def get_friend(self, jid):
        if self._onlineGrp.get(jid) != None :
            return self._onlineGrp[jid]
        elif self._offlineGrp.get(jid) != None:
            return self._offlineGrp[jid]
        return None

    def get_all(self):
        return dict(self._offlineGrp.items() + 
                self._onlineGrp.items())




