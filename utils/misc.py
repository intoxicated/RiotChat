""" 

helper classes 

"""

class MessageBuffer(object):
    def __init__(self):
        self.buf = []

    def push(self, msg_from, msg, time):
        entry = (msg_from, msg, time)
        self.buf.append(entry)

    def pop():
        if len(self.buf) != 0:
            return self.buf.pop(0)
        else:
            return None

"""

Misc enums

"""

class Division():
    NONE, I, II, III, IV, V = range(6)


class Tier():
    UNRANKED, BRONZE, SILVER, GOLD,\
    PLATINUM, DIAMOND, CHALLENGER = range(7)
    
class GameStatus():
    pass

class Queue():
    pass

"""

miscellous methods

"""

def jid2summoner(jId):
    pass

def summoner2jid(summonerId):
    pass



