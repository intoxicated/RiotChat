import sys

from core.riotxmpp_client import RiotXMPPClient

class RiotChat(object):
    pass

    #help
    #cmd analyze

if __name__ == "__main__":
    usr = sys.argv[0]
    pw = sys.argv[1]
    region = sys.argv[2]

    client = RiotXMPPClient()
    client.connect()

    while True:
        cmd = raw_input("RiotChat > ")
        #analyze command and do something
        if cmd == "send":
            client.send(id, msg)