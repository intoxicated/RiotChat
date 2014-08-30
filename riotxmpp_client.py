from riotxmpp.riotxmpp import RiotXMPP
from riotxmpp.utils.serverlist import *
from riotxmpp.models.cmds import *
from riotxmpp.models.user import User, Friend, RosterManager

import sys
import os
import re

"""
    extends RiotXMPP to provide full features 

"""

class RiotXMPPClient(RiotXMPP):
    def __init__(self, usrname, pw, region="NA", verbose=False):
        super(RiotXMPPClient, self).__init__(usrname, pw, region, verbose)
        
        #add additional handler
        self.add_event_handler("got_online", self.got_online)
        self.add_event_handler("got_offline", self.got_offline)
        self.add_event_handler("roster_update", self.roster_update)
        self.add_event_handler("on_message", self.on_message)
        self.add_event_handler("add_event", self.add_event)
        self.add_event_handler("remove_event", self.remove_event)
        self.add_event_handler("connected", self.connected)
        self.add_event_handler("disconnected", self.disconnected)
        self.add_event_handler("grp_invitation", self.grp_invitation)
        #
    
    def help(self):
        formatStr = ""
        for cmd, desc in cmdlst.items():
            formatStr += "{:>9} {:<15} {:<20}\n".format(cmd, desc[0], desc[1])
            if cmd == 'display':
                for dk, ddesc in desc[2].items():
                    formatStr += "{:>9} {:<5} {:<9} {:<40}\n".\
                        format("","@type",dk, ddesc)

        print formatStr

    def start(self):
        self.connect()

    def stop(self):
        self.disconnect()
    
    def quit(self):
        if self.verbose:
            print "Terminating the program.."
        exit()

    def on_message(self, kwargs):
        print "{:<} {:<} {}".format(kwargs['msgfrom'],
                kwargs['stamp'], kwargs['msg'])

    def got_online(self, summoner_id):
        pass

    def got_offline(self, summoner_id):
        pass

    def roster_update(self, roster_update):
        pass

    def add_event(self, summoner_id):
        pass

    def remove_event(self, presence):
        pass

    def connected(self):
        pass

    def disconnected(self):
        pass

    def grp_invitation(self, user, room):
        print "INVITE \"%s\" \"%s\"" % (user, room)
        self.send_muc_invitation(room, user, msg="Wanna talk to you")
        pass

    #command wappers 
    def send(self, to, msg):
        print "SEND \"%s\" \"%s\"" % (to, msg)

        self.send_message(to, msg, "chat")

    def spam(self, to, msg):
        pass 

    def add(self, summoner_id):
        if "@" not in summoner_id: #summoner name
            pass
        else:
            self.add_friend(summoner_id)

    def remove(self, summoner_id):
        if "@" not in summoner_id: #summoner name 
            pass
        else:
            self.remove_friend(summoner_id)

    def clear(self):
        os.system('clear')

    def display(self, args):
        print "ARGS TYPE: %s ARGS: %s" % \
                (type(args), args[0])
        if args[0] == 'all':
            self.display_all()
        elif args[0] == 'online':
            self.display_online()
        elif args[0] == 'history' and args[1] != None:
            self.display_history(args[1])
        elif args[0] == 'status' and args[1] != None:
            self.display_status(args[1])
        elif args[0] == 'rooms':
            self.display_rooms()
        else:
            print args
            print "invalid arguments for display"

    def display_rooms(self):
        for room, urs in self.mucs.items():
            print "Room Name: " + room 
            print "Participants: " + ",".join(str(urs))

    def display_all(self):
        #display all friends 
        flst = self.roster_manager.get_all()
        resultStr = ""
        for k,v in flst.items():
            resultStr += v.name + "\n"  
        
        print resultStr

    def display_online(self):
        #display online friends
        flst = self.roster_manager.onlineGrp
        resultStr = ""
        for k,v in flst.items():
            resultStr += v.name + "\n"
        
        print resultStr

    def display_history(self, jid):
        #display past # of messages with summoner, or grp
        print "DISPLAY HISTORY WITH %s" % jid
        pass

    def display_status(self, summoner):
        fentry = self.roster_manager.get(summoner)
        print fentry.get_status()

def parse_cmd(cmds):
    cmdlst = cmds.split(" ")
    args = None 
    if cmdlst[0] == "send" or cmdlst[0] == "add" or \
        cmdlst[0] == "invite" or cmdlst[0] == "remove":
        args = re.findall(r'\"(.+?)\"', cmds)
        return cmdlst[0], args

    if len(cmdlst) == 1:
        return cmdlst[0], None
    else:
        return cmdlst[0], cmdlst[1:]

if __name__ == "__main__":
    usr = sys.argv[1]
    pw = sys.argv[2]
    region = sys.argv[3]
    print usr,pw, region

    client = RiotXMPPClient(usr,pw,region, verbose=True)
    #client.start()

    while True:
        #handle command
        cmds = raw_input("RiotChat > ")
        if cmds == "":
            continue
        #parse cmds 
        cmd, args = parse_cmd(cmds)
        print "func: %s args: %s" % (cmd, args)
        
        if cmd == "send" and len(args) == 2:
            client.send(args[0], args[1])
        elif cmd == "start":
            client.start()
        elif cmd == "stop":
            client.stop()
        elif cmd == "clear":
            client.clear()
        elif cmd == "display":
            client.display(args)
        elif cmd == "add":
            pass
        elif cmd == "remove":
            pass
        elif cmd == "quit":
            client.quit() 
        elif cmd == "invite":
            client.grp_invitation(args[0], args[1])
        else:
            print "Cannot recognize command"
