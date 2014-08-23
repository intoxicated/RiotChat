"""

xmpp wrapper to privde functionalities of xmpp for Riotxmpp

"""
import logging
import sleekxmpp
import sys
import threading
import dns
import xmltodict

from collections import defaultdict

from models.riot_exception import *
from models.serverlist import *
from models.user import User, Friend, Roster

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
    def __init__(self, username, pw, region="NA", verbose=False):
        self.username = username
        self.pw = pw
        self.region = region
        self.verbose = verbose
        self.mucs = []
        self.commands = {}
        #check instance of region
        
        #init listing
        self.friendlist = {}
        self.online = {}
        self.grplst = {}
        self._chat_cache = {}
        self.user = User()
        self.roster = Roster()

        #setup logging
        if self.verbose:
            logging.basicConfig(level=logging.DEBUG,\
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

    def add_event_handler(self, event, func):
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

    def _trigger_event(self, event, **kwargs):
        """

        """
        if callable(getattr(self, "_event_"+event, None)):
            if kwargs.items():
                getattr(self, "_event_"+event)(kwargs)
            else:
                getattr(self, "_event_"+event)()

    def _start(self, event):
        self.xmpp.send_presence()
        self.xmpp.get_roster()

    def send_message(self, to, msg, msgType):
        self.xmpp.send_message(mto=str(to), mbody=str(msg), mtype=msgType)

    def _xmpp_failed_auth(self, data):
        """
            server has rejected the provided login credential
        """
        self._trigger_event("failed_auth", data=data)

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
            self._trigger_event("message", msgfrom=sender,\
                                msg=message, stamp=time)

    def connect(self):
        serverip = dns.resolver.query(RiotServer[self.region][0])
        if self.verbose:
            print "Attempting to connect %s", serverip

        if not serverip:
            #raise exception
            pass

        if self.xmpp.connect((str(serverip[0]), 5223), use_ssl=True):
            self.xmpp.process(block=False) 
            print "connect finished"
        else:
            raise RiotServerUnavailableError("server is not up")
        
        return True

    def _connected(self, data):
        if self.verbose:
            print "[RiotXMPP] connected to the server"
        self._trigger_event("connected")

    def disconnect(self):
        self.xmpp.disconnect(wait=True)

    def _disconnected(self, data):
        if self.verbose:
            print "[RiotXMPP] Disconnected from the server"
        self._trigger_event("disconnected")

    def _xmpp_update(self, roster):
        """ complete list of friends 
            supclass can handle this to expand its functionality
        """
        if self.verbose:
            print "UPDATE<ROSTER>\n"
        for item in roster['roster']:
            #print "id: %s name: %s substype: %s grp: %s" % 
            #(item['jid'],item['name'],item['subscription'],item['groups'])
            fentry = Friend(str(item['jid'])+"/xiff", item['name'], 
                item['subscription'], item['groups'])
            self.roster.add(fentry)
        self._trigger_event("roster_update", data=roster['roster'])

    def _xmpp_subscribe(self, presence):
        """ got add from xmpp
            update friend online 
            and its status 
            send out presence 
        """
        self._trigger_event("subscribe", data=presence)

    def _xmpp_unsubscribe(self, presence):
        """ got removal from xmpp 
            update friend online 
        """
        self._trigger_event("unsubscribe", data=presence)


    def _xmpp_online(self, presence):
        """ got online message from xmpp 
            update friend online list 
            send out presence message 
        """
        print "GOT ONLINE"
        if presence['from'] != self.xmpp.boundjid:
            #get entry for friend
            jid = presence['from']

            #update status
            status_dic = xmltodict.parse(presence['status'])
            self.roster.updateStatus(jid, status_dic['body'])
        self._trigger_event("online", data=presence)
        self.xmpp.send_presence(pto=presence['from'], ptype='chat',
                pstatus=None)

    def _xmpp_offline(self, presence):
        """ got offline message from xmpp
            update friend onine list 
        """
        self._trigger_event("offline", data=presence)

    def _xmpp_changed_status(self, presence):
        """ status of friend has been changed 
            need to update tables
        """
        if presence['from'] != self.xmpp.boundjid:
            pass  
        self._trigger_event("change_status", data=presence)

    def remove_friend(self, summoner_id):
        jid = summoner2jid(summoner_id)
        
        self.xmpp.del_roster_item(jid,\
                callback=self._trigger_event("remove_friend", data=summoner_id))
        
    def add_friend(self, summoner_id, groups=[]):
        jid = summoner2jid(summoner_id)
        
        self.xmpp.send_presence_subscription(pto=jid)
        self.xmpp.update_roster(jid, subscription='to', groups=groups,\
                callback=self._trigger_event("add_friend", data=summoner_id))

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
