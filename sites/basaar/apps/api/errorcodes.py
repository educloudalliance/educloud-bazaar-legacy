
# This file includes definitions to API's error codes in format of exceptions. Each exception class here
# inherits the DataException or RollbackException depending on if the exception will rollback all the changes.
# Every exception has three fields: http-status code, api-error code and
# human readable error message. Some of the exceptions take parameters to customize the message when
# exception is thrown.

class DataException(Exception):
    msg = ""
    httpStatus = 0
    apiCode = 0

    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class RollbackException(Exception):
    msg = ""
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class ProductTypeNotFound(RollbackException):
    msg = "Error: Product type with slug '{}' could not be found. To get a list of available types, call /api/producttypes"
    httpStatus = 400
    apiCode = 10
    def __init__(self, productType):
        self.msg = self.msg.format(productType)
    def __str__(self):
        return repr(self.msg)

class WrongAmountOfSubjects(RollbackException):
    msg = "Error: 1-5 subjects has to be specified. To get a list of available subjects, call /api/subjects"
    httpStatus = 400
    apiCode = 12
    def __init__(self):
        pass
    def __str__(self):
        return repr(self.msg)

class EachSubjectOnlyOnce(RollbackException):
    msg = "Error: Please define each subject only once."
    httpStatus = 400
    apiCode = 14
    def __init__(self):
        pass
    def __str__(self):
        return repr(self.msg)

class SubjectNotFound(RollbackException):
    msg = "Error: No such subject as in subject field: '{}' To get a list of available subjects, call /api/subjects"
    httpStatus = 400
    apiCode = 15
    def __init__(self, subject):
        self.msg = self.msg.format(subject)
    def __str__(self):
        return repr(self.msg)

class TooMuchTags(RollbackException):
    msg = "Error: More than 5 tags specified. Only 0-5 allowed."
    httpStatus = 400
    apiCode = 20
    def __init__(self):
        pass
    def __str__(self):
        return repr(self.msg)

class UrlIsEmpty(RollbackException):
    msg = "Error: The url is empty. Does it contain multiple slashes in row eg. '///'?"
    httpStatus = 400
    apiCode = 25
    def __init__(self):
        pass
    def __str__(self):
        return repr(self.msg)

class ObjectNotFound(RollbackException):
    msg = "Error: No such collection or materialItem with url: {}"
    httpStatus = 404
    apiCode = 30
    def __init__(self, url):
        self.msg = self.msg.format(url)
    def __str__(self):
        return repr(self.msg)

class MissingField(RollbackException):
    msg = "Error: Missing or invalid json-field: '{}' Operation canceled."
    httpStatus = 400
    apiCode = 40
    def __init__(self, fieldname):
        self.msg = self.msg.format(fieldname)
    def __str__(self):
        return repr(self.msg)

class InvalidDate(RollbackException):
    msg = "Error: ContributionDate field was in wrong format. Should be yyyy-mm-dd"
    httpStatus = 400
    apiCode = 45
    def __init__(self):
        pass
    def __str__(self):
        return repr(self.msg)

class IncorrectBooleanField(RollbackException):
    msg = "Error: Incorrect format in boolean field: '{}' Should be either 'true' or 'false'"
    httpStatus = 400
    apiCode = 46
    def __init__(self, fieldname):
        self.msg = self.msg.format(fieldname)
    def __str__(self):
        return repr(self.msg)

class ObjectAlreadyExists(RollbackException):
    msg = "Error: Can't post at '{}' because an object already exists in this URL."
    httpStatus = 403
    apiCode = 60
    def __init__(self, url):
        self.msg = self.msg.format(url)
    def __str__(self):
        return repr(self.msg)

class NoJSON(RollbackException):
    msg = "Error: No JSON data available."
    httpStatus = 400
    apiCode = 41
    def __init__(self):
        pass
    def __str__(self):
        return repr(self.msg)

class ItemOnPath(RollbackException):
    msg = "Error: There is an item in middle of the url-path. Item's can't have children."
    httpStatus = 403
    apiCode = 81
    def __init__(self):
        pass
    def __str__(self):
        return repr(self.msg)

class RootError(RollbackException):
    msg = "Error: Can't create new root nodes."
    httpStatus = 403
    apiCode = 82
    def __init__(self):
        pass
    def __str__(self):
        return repr(self.msg)

class AuthError(RollbackException):
    msg = "Error: You are not the owner of a node in path."
    httpStatus = 403
    apiCode = 83
    def __init__(self):
        pass
    def __str__(self):
        return repr(self.msg)

class CantUpdateCollection(RollbackException):
    msg = "Error: Target is not an item but a collection Only items can be updated."
    httpStatus = 403
    apiCode = 84
    def __init__(self):
        pass
    def __str__(self):
        return repr(self.msg)