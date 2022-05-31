from api.exceptions import BaseException


class ExceptionAllowedModels(BaseException):
    def __init__(self):
        self.status_code = 400
        self.content = {"message": "The number of allowed models reached the limit."}


class ExceptionUserNotFound(BaseException):
    def __init__(self):
        self.status_code = 400
        self.content = {"message": "User not found."}
