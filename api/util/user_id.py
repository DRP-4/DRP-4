from uuid import UUID, uuid4
from flask import request
from app import running_as_dev

# SameSite parameter for the SetCookie header. Should be strict if frontend and API run off one domain
samesite = 'None' if running_as_dev else 'Strict'

_cookies_user_id_key: str = "user_id"


def new_user_id() -> UUID:
    return uuid4()


def with_user_id(func):
    def wrapped():
        set_cookie = False
        id = None
        if _cookies_user_id_key in request.cookies:
            id = UUID(request.cookies[_cookies_user_id_key])
        else:
            id = new_user_id()
            set_cookie = True

        res = func(id)
        if set_cookie:
            res.set_cookie(_cookies_user_id_key, str(
                id), samesite=samesite, secure=True)

        return res

    wrapped.__name__ = func.__name__
    return wrapped
