class SmartJobException(Exception):
    """
    Base exception for SmartJob AI.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResumeParsingException(SmartJobException):
    pass


class JobLoadingException(SmartJobException):
    pass


class MatchingException(SmartJobException):
    pass


class RecommendationException(SmartJobException):
    pass


class AIServiceException(SmartJobException):
    pass