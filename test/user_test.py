import unittest 
from datetime import datetime
from models.user import User
from utils.misc import Division, Tier, GameStatus
from models.riot_exception import *

class UserTest(unittest.TestCase):

    def test_create_user(self):
        time = datetime.now()
        user = User()
        user.id = 38413
        user.profIcon = 3134
        user.revisionDate = time
        user.level = 30
        user.name = 'intoxicated'
        
        self.assertEquals(user.id, 38413)
        self.assertEquals(user.profIcon, 3134)
        self.assertEquals(user.revisionDate, time)
        self.assertEquals(user.level, 30)
        self.assertEquals(user.name, 'intoxicated')

    def test_constructor(self):
        time = datetime.now()
        user = User(38413, 'intoxicated', 3134, 30, time)
        
        self.assertEquals(user.id, 38413)
        self.assertEquals(user.profIcon, 3134)
        self.assertEquals(user.revisionDate, time)
        self.assertEquals(user.level, 30)
        self.assertEquals(user.name, 'intoxicated')

    def test_user_status(self):
        time = datetime.now()
        user = User(38413, 'intoxicated', 3134, 30, time)

        user.tier = Tier.BRONZE
        user.division = Division.I
        user.gameStatus = GameStatus()

        self.assertEquals(user.tier, 1)
        self.assertEquals(user.division, 1)
        self.assertEquals(user.gameStatus, 3)

    def test_invalid_args(self):
        user = User()
        
        def setStatus():
            user.status = 'afk'

        def setLevelLow():
            user.level = -1

        def setLevelHigh():
            user.level = 31

        self.assertRaises(RiotRangeError, setLevelHigh)
        self.assertRaises(RiotRangeError, setLevelLow)
        self.assertRaises(RiotRangeError, setStatus)
        
    def test_all_other(self):
        pass


if __name__ == '__main__':
    unittest.main()
