"""

xmpp wrapper to privde functionalities of xmpp for Riotxmpp

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

def command(*args, **kwargs):
    def decorate(function, hidden=False, name=None, needArgs=False):
        function._bot_command = True
        function._bot_command_name = name or function.__name__
        function._bot_command_need_args = needArgs
        return function
    if args:
        return decorate(args[0], **kwargs)
    else:
        return lambda function: decorate(function, **kwargs)

class RiotXMPP(object):
    def __init__(self, username, pw, region=Server.NA, verbose=False):
        self.username = username
        self.pw = pw
        self.region = region
        self.verbose = verbose
        self.mucs = []
        self.commands = {}
        #check instance of region
        
        #setup logging
        #if self.verbose:
        logging.basicConfig(level=logging.DEBUG, 
                format='%(levelname)-8s %(message)s')
        
        #initiaite xmpp instance 
        self.xmpp = sleekxmpp.ClientXMPP(username+"@pvp.net/xiff","AIR_"+pw)
        self.xmpp.add_event_handler("session_start", self._start)
        self.xmpp.add_event_handler("failed_auth", self._xmpp_failed_auth)
        self.xmpp.add_event_handler("message", self._xmpp_message)
        
        self.xmpp.add_event_handler("disconnected", self._disconnected)
        self.xmpp.add_event_handler("connected", self._connected)
        self.xmpp.add_event_handler("presence_unsubsribe", self._xmpp_unsubscribe)
        self.xmpp.add_event_handler("presence_subscribe", self._xmpp_subscribe)
        
        self.xmpp.add_event_handler("got_online", self._xmpp_online)
        self.xmpp.add_event_handler("got_offline", self._xmpp_offline)
        self.xmpp.add_event_handler("roster_update", self._xmpp_update)
        self.xmpp.add_event_handler("changed_status", self._xmpp_changed_status)

        #setup plugin
        self.xmpp.register_plugin('xep_0030') # service discovery
        #self.xmpp.register_plugin('xep_0004') # Data forms
        #self.xmpp.register_plugin('xep_0060') # pubsub
        self.xmpp.register_plugin('xep_0199') # xmpp ping 
        self.xmpp.register_plugin('xep_0045') # muc 
        self.xmpp.register_plugin('xep_0249') # muc invitation
        #search for decorators and add to list

    def add_event_handler(event, func):
        """ add custom event handler
            you can add custom even handler for following event:
            connected,
            disconnected,
            change_status,
            subscribe, unsubscribe,
            failed_auth,
            got_online,
            got_offline,
            remove_friend, add_friend,
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

    def send_message(self, to, msg, msgType):
        self.xmpp.send_message(mto=str(to), mbody=str(msg), mtype=msgType)

    def _xmpp_failed_auth(self, data):
        """
            server has rejected the provided login credential
        """
        self.trigger_event("failed_auth", data=data)

    def _xmpp_message(self, msg):
        """
            handling incoming xmpp message 

            type=chat       (normal chat)
            muc_invite=true (muc invitation)

        """
        
        sender = str(msg['from'])
        time = str(msg['stamp'])
        message = '%(body)s' % msg

        #group invitation
        if msg['type'] == 'normal' and msg['muc_invite'] == 'true':
            inviter = msg['inviter'] 
            reason = '%(reason)s' % msg
            roomid = sender
            #join or not
            pass
        #group message
        elif msg['type'] in ('normal') and "~" in sender:
            pass
        #normal chat
        elif msg['type'] in ('chat'):
            #msg.reply('Thanks for sending\n%(body)s' % msg).send()
            self.trigger_event("message", msgfrom=sender, msg=message, stamp=time)

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
        if self.verbose:
            print "[RiotXMPP] connected to the server"
        self.trigger_event("connected")

    def disconnect(self):
        self.xmpp.disconnect(wait=True)

    def _disconnected(self, data):
        if self.verbose:
            print "[RiotXMPP] Disconnected from the server"
        self.trigger_event("disconnected")

    def _xmpp_update(self, roster):
        """ complete list of friends 
            supclass can handle this to expand its functionality
        """
        self.trigger_event("roster_update", data=roster)

    def _xmpp_subscribe(self, presence):
        """ got add from xmpp
            update friend online 
            and its status 
            send out presence 
        """
        self.trigger_event("subscribe", data=presence)

    def _xmpp_unsubscribe(self, presence):
        """ got removal from xmpp 
            update friend online 
        """
        self.trigger_event("unsubscribe", data=presence)


    def _xmpp_online(self, presence):
        """ got online message from xmpp 
            update friend online list 
            send out presence message 
        """
        self.trigger_event("online", data=presence)
        self.xmpp.send_presence(pto=presence['from'], ptype='chat',pstatus=None)
        if self.greeting is not None:
            self.send_message(presence['from'], self.greeting, "chat")

    def _xmpp_offline(self, presence):
        """ got offline message from xmpp
            update friend onine list 
        """
        self.trigger_event("offline", data=presence)

    def _xmpp_changed_status(self, presence):
        """ status of friend has been changed 
            need to update tables
        """
        self.trigger_event("change_status", data=presence)

    def remove_friend(self, summoner_id):
        jid = summoner2jid(summoner_id)
        
        self.xmpp.del_roster_item(jid,\
                callback=self.trigger_event("remove_friend", data=summoner_id))
        
    def add_friend(self, summoner_id, groups=[]):
        jid = summoner2jid(summoner_id)
        
        self.xmpp.send_presence_subscription(pto=jid)
        self.xmpp.update_roster(jid, subscription='to', groups=groups,\
                callback=self.trigger_event("add_friend", data=summoner_id))

    def send_muc_invitation(self, roomname, summoner_id, msg):
        jid = summoner2jid(summoner_id)
        room = "pr" + "~" + hashlib.sha1(roomname.encode()).hexdigest() +\
                "@" + "conference.pvp.net"

        self.xmpp.plugin['xep_0249'].send_invitation(jid, room, reason=msg)
        
        return (roomname, room, jid)

    def join_muc_room(self, room):
        roomid = room + "/" + self.username
        self.xmpp.send_presence(pto=roomid, pshow='groupchat')

    def leave_muc_room(self, room):
        roomid = room + "/" + self.username
        self.xmpp.send_presence(pto=roomid, pshow='unavailable')
