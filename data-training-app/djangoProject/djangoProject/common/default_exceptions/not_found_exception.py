class NotFoundException(Exception):
    def __init__(self, message, reason):
        super().__init__(message)
        self.reason = reason
        self.i18nKey = "NOT_FOUND"
