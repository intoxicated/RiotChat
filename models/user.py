""" 
User represents a user of lol player
"""
#from utils.misc import Division, Tier

from models.riot_exception import *

defaultStatus = { 
    'level': 100,
    'profileIcon': 673,
    'wins': 0,
    'leaves': 0,
    'odinWins': 0,
    'odinLeaves': 0,
    'queueType' : '/',
    'rankedLosses': 0,
    'rankedRating': 0,
    'tier': 'UNRANKED',
    'rankedLeagueName': 'Singed&amp;apos;s Butchers',
    'rankedLeagueDivision': 'I',
    'rankedLeagueTier': 'DIAMOND',
    'rankedLeageuQueue': 'RANKED_SOLO_5X5',
    'rankedWins': 0,
    'gameStatus': 'outOfGame',
    'statusMsg': 'PyRiotChat Client',
}

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
    def __init__(self, jid, name, res, status=defaultStatus):
        self._jid = jid
        self._name = name
        self._resource = res
        self._status = status # Status()
    
    @property
    def jid(self):
        return self._jid
    
    @jid.setter
    def jid(self, jid):
        self._jid = jid

    @property 
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, newresource):
        self._resource = newresource

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
    
    def form_status(self):
        formStatus = ""
        for key, value in self._status.items():
            if value != None:
                formStatus += "<" + str(key) + ">" +\
                    str(value) + "</" + str(key) + ">"
        return formStatus

    def get_status(self):
        formatStr = ""
        
        for k,v in self._status.items():
            formatStr += "{:<10} {:<10}".format(k,v)
        return formatStr

class Friend(User):

    def __init__(self, jid, res, name, substype, grpName, status=None):
        super(Friend, self).__init__(jid, name, res, status)
        self._groupName = 'Default' if (grpName == '**Default') else grpName
        self._substype = substype
        self._online = False 
        
    @property
    def groupName(self):
        return self._groupName
    
    @groupName.setter
    def groupName(self, value):
        self._groupName = value

    @property
    def online(self):
        return self._isOnline

    @online.setter
    def online(self, online):
        self._isOnline = online


class RosterManager(object):
    def __init__(self):
        #key name : value (Friend object)
        self._offlineGrp = {}
        self._onlineGrp = {}
    
    @property
    def offlineGrp(self):
        return self._offlineGrp

    @property
    def onlineGrp(self):
        return self._onlineGrp

    def add(self, summoner, online=False):
        if not isinstance(summoner, Friend):
            raise Exception
        if not online:
            self._offlineGrp[summoner.jid] = summoner
        else: 
            self._onlineGrp[summoner.jid] = summoner

    def is_friend(self, jid):
        if self._offlineGrp.get(jid) or self._onlineGrp.get(jid):
            return True
        else:
            return False

    def updateStatus(self, jid, resource, status, online=False):
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
            fentry.resource = resource
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
    
    def summoner2jid(self, summoner):
        for k,v in self._onlineGrp.items():
            if v.name == summoner:
                return k
        
        for k,v in self._offlineGrp.items():
            if v.name == summoner:
                return k
    
        return None

    def jid2summoner(self, jid):
        if self._onlineGrp.get(jid) != None:
            return self._onlineGrp[jid].name
        elif self._offlineGrp.get(jid) != None:
            return self._offlineGrp[jid].name
        else:
            pass # exception or use riot api to find name 

    def get_friend(self, jid):
        if self._onlineGrp.get(jid) != None :
            return self._onlineGrp[jid]
        elif self._offlineGrp.get(jid) != None:
            return self._offlineGrp[jid]
        return None

    def get_all(self):
        return dict(self._offlineGrp.items() + 
                self._onlineGrp.items())

    


