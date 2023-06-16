from uuid import UUID, uuid4
from flask import request, abort, Response
from app import running_as_dev

# SameSite parameter for the SetCookie header. Should be strict if frontend and API run off one domain
samesite = "None" if running_as_dev else "Strict"

_cookies_user_id_key: str = "user_id"


def new_user_id() -> UUID:
    return uuid4()


def with_user_id(func):
    def wrapped():
        set_cookie = False
        id = None
        if _cookies_user_id_key in request.cookies:
            try:
                id = UUID(request.cookies[_cookies_user_id_key])
            except ValueError:
                abort(400)
        else:
            id = new_user_id()
            set_cookie = True

        res = func(id)
        if set_cookie:
            if isinstance(res, tuple):
                res = Response(res[0], status=res[1])

            res.set_cookie(
                _cookies_user_id_key, str(id), samesite=samesite, secure=True
            )

        return res

    wrapped.__name__ = func.__name__
    return wrapped
