"""
riot xmpp wrapper to provide basic features
connect, disconnect, send_message, and receving message

"""
import logging
import sleekxmpp
import sys
import threading
import dns

from models.riot_exception import *
from models.serverlist import *

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

class RiotXMPP(object):
    def __init__(self, username, pw, region=Server.NA, verbose=False):
        self.username = username
        self.pw = pw
        self.region = region
        self.verbose = verbose
        #check instance of region

        #setup logging
        #if self.verbose:
        logging.basicConfig(level=logging.DEBUG, 
                format='%(levelname)-8s %(message)s')
        
        #initiaite xmpp instance 
        self.xmpp = sleekxmpp.ClientXMPP(username+"@pvp.net/xiff","AIR_"+pw)
        self.xmpp.add_event_handler("session_start", self.start)
        self.xmpp.add_event_handler("message", self.xmmp_message)
        self.xmpp.add_event_handler("disconnected", self._disconnected)
        self.xmpp.add_event_handler("connected", self._connected)

        #setup plugin
        self.xmpp.register_plugin('xep_0030') # service discovery
        self.xmpp.register_plugin('xep_0004') # Data forms
        self.xmpp.register_plugin('xep_0060') # pubsub
        self.xmpp.register_plugin('xep_0199') # xmpp ping 
        
    def add_event_handler(event, func):
        """ add custom event handler
            you can add custom even handler for following event:
            connected,
            disconnected,
            change_status,
            change_subscription,
            failed_auth,
            got_online,
            got_offline,
            groupchat_subject/precense/message,
            presence_available/unavailable/subscribe(d)/unsubscribe(d)
            message,
            roster_update
        """
        if callable(func):
            setattr(self, "_event_"+event, func)
        else:
            raise RiotInvalidValueError("invalid event handler")

    def trigger_event(self, event, **kwargs):
        """

        """
        if callable(getattr(self, "_event_"+event, None)):
            if kwargs.items():
                getattr(self, "_event_"+event)(kwargs)
            else:
                getattr(self, "_event_"+event)()

    def start(self, event):
        self.xmpp.send_presence()
        self.xmpp.get_roster()

    def xmpp_message(self, msg):
        """
            handling incoming xmpp message 

        """
        if msg['type'] in ('chat', 'normal'):
            msg.reply('Thanks for sending\n%(body)s' % msg).send()

    def connect(self):
        serverip = dns.resolver.query(RiotServer[self.region][0])
        
        if not serverip:
            #raise exception
            pass

        if self.xmpp.connect((str(serverip[0]), 5223), use_ssl=True):
            self.xmpp.process(block=False) 
            print "connect finished"
        else:
            raise RiotServerUnavailableError("disable to connect to server")
        
        return True

    def _connected(self, data):
        pass
   
    def disconnect(self):
        self.xmpp.disconnect(wait=True)

    def _disconnected(self, data):
        if self.verbose:
            print "[RiotXMPP] Disconnected from the server"

