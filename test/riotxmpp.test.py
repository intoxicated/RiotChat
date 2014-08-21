import unittest
from models.serverlist import *
from core.riotxmpp import RiotXMPP

user = "arahsi8318"
pw = "wjdgkdms1218"

class TestBasicChatCore(unittest.TestCase):

    def test_connect_server(self):
        core = RiotXMPP(user, pw, region=Server.NA, verbose=True)       
        didConnect = core.connect()

        self.assertTrue(didConnect)
        core.disconnect()
"""    
class BasicChatCoreTest(unittest.TestCase):
    def setUp(self):
        self.core = RiotXMPP(user,pw)

    def tearDown(self):
        self.core.disconnect()

class TestChatCoreFeatures(BasicChatCoreTest):
    
    def test_send_msg(self):
        self.core.send_message(to="id", msg="msg")
        
        #check return value

    def test_add_event_handler(self):
        def on_message():
            print msg + "has been sent out"

        event = "send_message"
        self.core.add_event_handler(event, on_message)
        self.assertEquals(self.core._event_send, on_message)

    def test_add_event_handler_with_kwargs(self):
        def on_failed_auth(msg):
            print msg + "to authenticated"
        
        event = "failed_auth"

        self.core.add_event_handler(event, on_failed_auth, msg="failed")
        self.assertEquals(self.core._event_failed_auth, on_failed_auth)

"""
if __name__ == "__main__":
    unittest.main()
