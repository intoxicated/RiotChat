from riotxmpp import RiotXMPP
from models.serverlist import *

import sys

"""
    extends RiotXMPP to provide full features 

"""
cmdlst = { "send":("<to> <msg>", "send message to destine user/grp"),
            "add":("<summoner_id>", "add summoner to your friend list"),
            "remove":("<summoner_id>", "remove summoner from your friend list"),
            "display":("<type> <opt>", "display options", 
                    {"all": "display all your friends from list",
                        "online":"display only online friends from list",
                        "history":"display # of chat history associated with summoner"}
            ),
            "invite":("<to>", "send group chat invitation to summoner"),
}

class RiotXMPPClient(RiotXMPP):
    def __init__(self, usrname, pw, region="NA", verbose=False):
        super(RiotXMPPClient, self).__init__(usrname, pw, region, verbose)
        
        #add additional handler
        self.add_event_handler("got_online", self.got_online)
        self.add_event_handler("got_offline", self.got_offline)
        self.add_event_handler("roster_update", self.roster_update)
        self.add_event_handler("message", self.on_message)
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

    def on_message(self, msgfrom, msg, stamp, origin=None):
        print "INCOMING MSG:"
        print "{:<20} {:<20} {}".format(msgfrom, stamp, msg)

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

    def grp_invitation(self):
        #join room
        pass

    #command wappers 
    def send(self, to, msg):
        if self.verbose:
            print "SEND %s %s" % (to, msg)

        self.send_message(to, msg, "chat")

    def add(self, summoner_id):
        self.add_friend(summoner_id)

    def remove(self, summoner_id):
        self.remove_friend(summoner_id)

    def display(self, t):
        print "ARGS TYPE: %s ARGS: %s F: %s" % (type(t), t, t[0])
        if t[0] == 'all':
            self.display_all()
        elif t[0] == 'online':
            self.display_online()
        elif t[0] == 'history' and t[1] != None:
            self.display_history(t[1])
        else:
            print t
            print "invalid arguments for display"

    def display_all(self):
        #display all friends 
        print "DISPLAY ALL"
        pass
    
    def display_online(self):
        #display online friends
        print "DISPLAY ONLINE"
        pass

    def display_history(self, jid):
        #display past # of messages with summoner, or grp
        print "DISPLAY HISTORY WITH %s" % jid
        pass


def parse_cmd(cmds):
    cmdlst = cmds.split(" ")

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
        if callable(getattr(client, cmd, None)):
            try:
                if args:
                    getattr(client, cmd)(args)
                else:
                    getattr(client, cmd)()
            except TypeError:
                print "invalid arguments, try use help"
        else:
            print "Cannot recognize command"
