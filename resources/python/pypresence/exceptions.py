class PyPresenceException(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = 'An error has occurred within PyPresence'
        super().__init__(message)


class DiscordNotFound(PyPresenceException):
    def __init__(self):
        super().__init__('Could not find Discord installed and running on this machine.')


class InvalidPipe(PyPresenceException):
    def __init__(self):
        super().__init__('Pipe Not Found - Is Discord Running?')


class InvalidArgument(PyPresenceException):
    def __init__(self, expected, received, description: str = None):
        description = '\n{0}'.format(description) if description else ''
        super().__init__('Bad argument passed. Expected {0} but got {1} instead{2}'.format(expected, received,
                                                                                           description)
                         )


class ServerError(PyPresenceException):
    def __init__(self, message: str):
        super().__init__(message.replace(']', '').replace('[', '').capitalize())


class DiscordError(PyPresenceException):
    def __init__(self, code: int, message: str, override=False):
        self.code = code
        self.message = message
        super().__init__('Error Code: {0} Message: {1}'.format(code, message) if not override else message)


class InvalidID(DiscordError):
    def __init__(self):
        super().__init__(4000, 'Client ID is Invalid')


class ArgumentError(PyPresenceException):
    def __init__(self):
        super().__init__('Supplied function must have one argument.')


class EventNotFound(PyPresenceException):
    def __init__(self, event):
        super().__init__('No event with name {0} exists.'.format(event))


class PipeClosed(PyPresenceException):
    def __init__(self):
        super().__init__('The pipe was closed. Catch this exception and re-connect your instance.')


class ResponseTimeout(PyPresenceException):
    def __init__(self):
        super().__init__('No response was received from the pipe in time')


class ConnectionTimeout(PyPresenceException):
    def __init__(self):
        super().__init__('Unable to create a connection to the pipe in time')
