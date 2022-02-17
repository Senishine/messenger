from common.messages import MessageType, ClientRequestFieldName, UserFieldName, MsgFieldName, ResponseCode, \
    ServerResponseFieldName, RequestToServer, AuthenticateFieldName
from log.server_log_config import logging
from server.repository import Repository

logger = logging.getLogger('gb.server')


def validate_authenticate(msg) -> str:
    if not msg:
        return "Empty message"
    if msg.get(ClientRequestFieldName.ACTION.value) != MessageType.AUTHENTICATE.value:
        return f"Message type is not {MessageType.AUTHENTICATE.value}"
    if not msg.get(UserFieldName.USER.value) or \
            not msg.get(UserFieldName.USER.value).get(UserFieldName.ACCOUNT.value):
        return "Account name is not filled"
    if not msg.get(UserFieldName.USER.value).get(AuthenticateFieldName.PASSWORD.value):
        return "Password is not filled"
    return ""


def validate_sign_up(msg) -> str:
    if not msg:
        return "Empty message"
    if msg.get(ClientRequestFieldName.ACTION.value) != MessageType.SIGN_UP.value:
        return f"Message type is not {MessageType.SIGN_UP.value}"
    if not msg.get(UserFieldName.USER.value):
        return "User information is not filled"
    if not msg.get(UserFieldName.USER.value).get(UserFieldName.LOGIN.value):
        return "Login is not filled"
    if not msg.get(UserFieldName.USER.value).get(AuthenticateFieldName.PASSWORD.value):
        return "Password is not filled"
    if not msg.get(UserFieldName.USER.value).get(UserFieldName.NAME.value):
        return "Name is not filled"
    if not msg.get(UserFieldName.USER.value).get(UserFieldName.SURNAME.value):
        return "Surname is not filled"
    if not msg.get(UserFieldName.USER.value).get(UserFieldName.BIRTHDATE.value):
        return "Birthdate is not filled"
    return ""


def validate_presence(msg) -> str:
    if not msg:
        return "Empty message"
    if msg.get(ClientRequestFieldName.ACTION.value) != MessageType.PRESENCE.value:
        return f"Message type is not {MessageType.PRESENCE.value}"
    if not msg.get(UserFieldName.USER.value) or \
            not msg.get(UserFieldName.USER.value).get(UserFieldName.ACCOUNT.value):
        return "Account name is not filled"
    return ""


def validate_add_contact(msg, account) -> str:
    if not msg:
        return "Empty message"
    if msg.get(ClientRequestFieldName.ACTION.value) != MessageType.ADD_CONTACT.value:
        return f"Message type is not {MessageType.ADD_CONTACT.value}"
    if not msg.get(RequestToServer.USER_ID.value) or \
            not msg.get(RequestToServer.USER_LOGIN.value):
        return "Login is not filled"
    if msg.get(RequestToServer.USER_ID.value) != account:
        return "'User_id' field is not equal logged in user"
    return ""


def validate_del_contact(msg, account) -> str:
    if not msg:
        return "Empty message"
    if msg.get(ClientRequestFieldName.ACTION.value) != MessageType.DEL_CONTACT.value:
        return f"Message type is not {MessageType.DEL_CONTACT.value}"
    if not msg.get(RequestToServer.USER_ID.value) or \
            not msg.get(RequestToServer.USER_LOGIN.value):
        return "Login is not filled"
    if msg.get(RequestToServer.USER_ID.value) != account:
        return "'User_id' field is not equal logged in user"
    return ""


def validate_get_contact(msg, account) -> str:
    if not msg:
        return "Empty message"
    if msg.get(ClientRequestFieldName.ACTION.value) != MessageType.GET_CONTACTS.value:
        return f"Message type is not {MessageType.GET_CONTACTS.value}"
    if not msg.get(RequestToServer.USER_LOGIN.value):
        return "Login is not filled"
    if msg.get(RequestToServer.USER_LOGIN.value) != account:
        return "'User_id' field is not equal logged in user"
    return ""


def validate_user_msg(msg, account) -> str:
    if not msg:
        return "Empty message"
    if msg.get(ClientRequestFieldName.ACTION.value) != MessageType.MESSAGE.value:
        return f"Message type is not {MessageType.MESSAGE.value}"
    if not msg.get(MsgFieldName.TO.value):
        return "No 'to' field"
    if not msg.get(MsgFieldName.MESSAGE.value):
        return "No 'message' field"
    if msg.get(MsgFieldName.FROM.value) != account:
        return "'From' field is not equal logged in user"
    return ""


def create_response(code=ResponseCode.OK.value, msg=None):
    logger.info('Creating response for client [code=%s, msg=%s]', code, msg)
    assert isinstance(code, int), 'code is not an integer'
    data = {
        ServerResponseFieldName.RESPONSE.value: code
    }

    if msg is None:
        return data
    if 400 <= code <= 600:
        data[ServerResponseFieldName.ERROR.value] = msg
    else:
        data[ServerResponseFieldName.ALERT.value] = msg

    return data


def remove_if_present(key, d: dict):
    value = d.get(key)
    if value is not None:
        del d[key]


def remove_from_list(obj, l: list):
    try:
        l.remove(obj)
    except ValueError:
        pass

