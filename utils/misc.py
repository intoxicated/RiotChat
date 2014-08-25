""" 

helper classes 

"""

class MessageBuffer(object):
    def __init__(self, maxSize):
        self.buf = []
        self.i = -1

    def push(self, msg_from, msg, time):
        if len(self.buf) > maxSize:
            self.buf.pop(0)

        entry = (msg_from, msg, time)
        self.buf.append(entry)

    def pop():
        if len(self.buf) > 0:
            return self.buf.pop(0)
        else:
            return None

    def __getitem__(self, sliced):
        return self.buf[sliced]

    def __iter__(self):
        return self

    def next(self):
        if self.i < len(self.buf)-1:
            self.i += 1
            return self.buf[self.i]
        else:
            raise StopIteration

"""

miscellous methods

"""

def jid2summoner(rosterobj, jid, online):
    pass
    
def summoner2jid(summonerId):
    pass





