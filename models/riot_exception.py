"""


"""

class RiotException(Exception):
    def __init__(self, msg):
        super(RiotException, self).__init__(msg)
        self.msg = msg

class RiotValueException(RiotException):
    pass

class RiotRangeError(RiotValueException):
    pass

class RiotInvalidValueError(RiotValueException):
    pass



class RiotServerException(RiotException):
    pass

class RiotNameDoesNotExists(RiotServerException):
    pass 

class RiotOperationFailError(RiotServerException):
    pass

class RiotDisconnectError(RiotServerException):
    pass

class RiotRateLimitedError(RiotServerException):
    pass


