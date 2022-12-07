import base64
from db import User, Session
from werkzeug.security import generate_password_hash, check_password_hash
from errors import ApiException


def hash_password(password: str):
    hashed = generate_password_hash(password)
    return hashed


def get_username_password_from_authdata(auth_from_headers):
    """ Получаем username и password из headers"""
    auth_data = auth_from_headers.split()[1]
    un_h, psw_h = base64.b64decode(auth_data.encode()).decode().split(':')
    return un_h, psw_h


def is_authenticated(username, password):
    """Проверка аутентификации"""
    with Session() as session:
        user = session.query(User).filter(User.username == username).first()
        if user and check_password_hash(user.password, password):
            return user.id
        else:
            raise ApiException(403, 'wrong username or password')


def total_check_authentication(auth_from_headers):
    username, password = get_username_password_from_authdata(auth_from_headers)
    user_id = is_authenticated(username, password)
    return user_id
