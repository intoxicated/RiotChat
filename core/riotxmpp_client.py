from riotxmpp import RiotXMPP
from models.user import User, Friend
from models.serverlist import *
from utils.misc import MessageBuffer
from utils.misc import Division, Tier

"""
    extends RiotXMPP to provide full features 

"""

class RiotXMPPClient(RiotXMPP):
    def __init__(self, usrname, pw, region=Server.NA, verbose=False):
        super(RiotXMPPClient, self).__init__(usrname, pw, region, verbose)

        #add additional handler
    
    
    

