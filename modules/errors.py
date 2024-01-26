from . import Constants

class InvalidInputError(Exception):
    """Raised when the input format is invalid."""
    def __init__(self, msg):
        print(msg)
        print('Valid extensions:', ','.join(Constants.FILE_FORMATS))
        exit()

class InvalidSyntax(Exception):

    def __init__(self, msg):
        print(msg)
        print('Please check file content.')
        exit()

class InvalidArg(Exception):

    def __init__(self, msg):
        print(msg)
        exit()