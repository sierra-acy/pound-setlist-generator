class TrackNotFoundError(Exception):
    """Exception raised for errors in the availability of a track to satisfy requirements.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)

class DuplicateIDError(Exception):
    """ Exception raised when an ID is duplicated in a set of tracks.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)
