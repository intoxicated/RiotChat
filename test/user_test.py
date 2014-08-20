import unittest 
from datetime import datetime
from models.user import User
from models.riot_exception import RiotInvalidRangeError

class UserTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_user(self):
        time = datetime.now()
        user = User()
        user.id = 38413
        user.profIcon = 3134
        user.revisionDate = time
        user.level = 30
        user.name = 'intoxicated'
        user.tier = 'BRONZE'
        user.division = 'I'

        self.assertEquals(user.id, 38413)
        self.assertEquals(user.profIcon, 3134)
        self.assertEquals(user.revisionDate, time)
        self.assertEquals(user.level, 30)
        self.assertEquals(user.name, 'intoxicated')

    def test_constructor(self):
        time = datetime.now()
        user = User(38413, 'intoxicated', 3134, 30, time)
        user.status = 'away'
        
        self.assertEquals(user.status, 'away')
        self.assertEquals(user.id, 38413)
        self.assertEquals(user.profIcon, 3134)
        self.assertEquals(user.revisionDate, time)
        self.assertEquals(user.level, 30)
        self.assertEquals(user.name, 'intoxicated')

    def test_invalid_args(self):
        user = User()
        
        def setStatus():
            user.status = 'afk'

        def setLevelLow():
            user.level = -1

        def setLevelHigh():
            user.level = 31

        self.assertRaises(RiotInvalidRangeError, setLevelHigh)
        self.assertRaises(RiotInvalidRangeError, setLevelLow)
        self.assertRaises(RiotInvalidRangeError, setStatus)
        
    def test_all_other(self):
        pass


if __name__ == '__main__':
    unittest.main()
