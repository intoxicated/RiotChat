"""

xmpp wrapper to privde functionalities of xmpp for Riotxmpp

"""
import logging
import sleekxmpp
import sys
import threading
import dns
import xmltodict
import datetime

from collections import defaultdict

import models.riot_exception as rioterror
from models.serverlist import *
from models.user import User, Friend, RosterManager

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
        self._chat_cache = {}
        self.user = User(None, None, "/xiff")
        self.roster_manager = RosterManager()

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
        self.xmpp.add_event_handler("presence_unsubsribe", 
                                        self._xmpp_unsubscribe)
        self.xmpp.add_event_handler("presence_subscribe", 
                                        self._xmpp_subscribe)
        
        self.xmpp.add_event_handler("got_online", self._xmpp_online)
        self.xmpp.add_event_handler("got_offline", self._xmpp_offline)
        self.xmpp.add_event_handler("roster_update", self._xmpp_update)
        self.xmpp.add_event_handler("changed_status", 
                                        self._xmpp_changed_status)

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
        if self.verbose:
            print "<RiotDEBUG> ADDING HANDLER " + event + " " + \
                    func.func_name

        if callable(func):
            setattr(self, "_event_"+event, func)
        else:
            raise rioterror.RiotInvalidValueError("invalid event handler")

    def _trigger_event(self, event, **kwargs):
        """

        """
        if self.verbose:
            print "<RiotDEBUG> TRIGGER " + event + " with "
            print kwargs

        if callable(getattr(self, "_event_"+event, None)):
            if kwargs.items():
                getattr(self, "_event_"+event)(**kwargs)
            else:
                getattr(self, "_event_"+event)()

    def _start(self, event):
        self.user.jid = str(self.xmpp.boundjid).split("/")[0]
        self.user.resource = str(self.xmpp.boundjid).split("/")[1]
       
        if self.verbose:
            print "<RiotDEBUG> jid: %s resource: %s" % \
                        (self.user.jid, self.user.resource)
        self.xmpp.send_presence(pshow='chat',
                            pstatus=self.user.form_status())
        self.xmpp.get_roster()

    def send_message(self, to, msg, msgType):
        jid = self.roster_manager.summoner2jid(to)
        if jid != None:
            self.xmpp.send_message(mto=str(jid), mbody=str(msg), 
                                                mtype=msgType)

    def send_all(self, msg):
        for u,v in self.roster_manager.onlineGrp.items():
            self.xmpp.send_message(mto=u+v.resource,mbody=msg,
                    mtype='chat',mfrom=self.xmpp.boundjid)

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
        
        jid = str(msg['from']).split("/")[0]
        sender = self.roster_manager.jid2summoner(jid)
        time = str(datetime.datetime.now())
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
            print "%s %s %s" % (sender, message, time)
            self._trigger_event("on_message", msgfrom=sender, msg=message, stamp=time)

    def connect(self):
        serverip = dns.resolver.query(RiotServer[self.region][0])
        if self.verbose:
            print "Attempting to connect %s", serverip

        if not serverip:
            raise rioterror.RiotBadRequestError("Server ip was not found")

        if self.xmpp.connect((str(serverip[0]), 5223), use_ssl=True):
            self.xmpp.process(block=False) 
            print "connect finished"
        else:
            raise rioterror.RiotServerUnavailableError("server is not up")
        
        return True

    def _connected(self, data):
        if self.verbose:
            print "<RiotDEBUG> connected to the server"
        self._trigger_event("connected")

    def disconnect(self):
        self.xmpp.disconnect(wait=True)

    def _disconnected(self, data):
        if self.verbose:
            print "<RiotDEBUG> Disconnected from the server"
        self._trigger_event("disconnected")

    def _xmpp_update(self, roster):
        """ complete list of friends 
            supclass can handle this to expand its functionality
        """

        if self.verbose:
            print "<RiotDEBUG> UPDATE ROSTER\n"
            #rosterlst = ""
            #for k,v in self.roster_manager.get_all().items():
            #    rosterlst += "%s ||" % k
            #print rosterlst
        
        for item in roster['roster']:
            #print "id: %s name: %s substype: %s grp: %s" % 
            #(item['jid'],item['name'],item['subscription'],item['groups'])
            fentry = Friend(str(item['jid']), None, item['name'], 
                item['subscription'], item['groups'])
            self.roster_manager.add(fentry)
        

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
        print "<RiotDEBUG> : ROUTINE GOT ONLINE"
        
        jid = str(presence['from']).split("/")[0]
        resource = str(presence['from']).split("/")[1]
        
        #ignore if oneway subscription
        if not self.roster_manager.is_friend(jid):
            return None
        
        if self.verbose and presence['from'] != self.xmpp.boundjid:
            print "<RiotDEBUG> " + self.roster_manager.jid2summoner(
                    jid) + " is online"
            print "<RiotDEBUG> " + "resource is " + resource
        if presence['from'] != self.xmpp.boundjid:
            #update status
            status_dic = xmltodict.parse(presence['status'])
            self.roster_manager.updateStatus(jid, resource,
                             status_dic['body'], online=True)
            self.xmpp.send_presence(pto=presence['from'], ptype='chat',
                pstatus=self.user.form_status())
            self._trigger_event("online", data=presence)


    def _xmpp_offline(self, presence):
        """ got offline message from xmpp
            update friend onine list 
        """
        if self.verbose:
            print "<RiotDEBUG> OFFLINE" + \
                    str(presence['from']) + " is offline now"

        if presence['from'] != self.xmpp.boundjid:
            jid = str(presence['from']).split("/")[0]
            self.roster_manager.updateStatus(jid, None,None, online=False)
            self._trigger_event("offline", data=presence)

    def _xmpp_changed_status(self, presence):
        """ status of friend has been changed 
            need to update tables
        """
        if presence['from'] != self.xmpp.boundjid and self.verbose:
            
            jid = str(presence['from']).split("/")[0]
            name = self.roster_manager.jid2summoner(jid)
            print "<RiotDEBUG> CHAGE: "+ name + "(" + \
                str(presence['from']) + ")"+" has been changed its status"

        if presence['from'] != self.xmpp.boundjid:
            jid = str(presence['from']).split("/")[0]
            resource = str(presence['from']).split("/")[1]
            #need to handle off line status == None
            status_dic = xmltodict.parse(presence['status'])
            self.roster_manager.updateStatus(jid, resource, 
                            status_dic['body'], online=True)

            self._trigger_event("change_status", data=presence)

    def remove_friend(self, summoner):
        jid = self.roster_manager.summoner2jid(summoner)
        if jid == None:
            print "<RiotError> Cannot remove a friend not in list"
            
        self.roster_manager.remove(jid)
        self.xmpp.del_roster_item(jid,\
            callback=self._trigger_event("remove_friend", data=summoner_id))
        
    def add_friend(self, summoner_id, groups=[]):
        jid = summoner2jid(summoner_id)
       
        #self.roster_namager
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
