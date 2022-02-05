from enum import Enum


class ClientRequestFieldName(Enum):
    ACTION = 'action'


class MsgFieldName(Enum):
    FROM = 'from'
    TO = 'to'
    MESSAGE = 'message'


class PresenceFieldName(Enum):
    USER = 'user'
    ACCOUNT = 'account_name'


class ServerResponseFieldName(Enum):
    RESPONSE = 'response'
    TIME = 'time'
    ALERT = 'alert'
    ERROR = 'error'


class MessageType(Enum):
    PRESENCE = 'presence'
    MESSAGE = 'msg'
    GET_CONTACTS = 'get_contacts'
    ADD_CONTACT = 'add_contact'
    DEL_CONTACT = 'del_contact'


class ResponseCode(Enum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500
