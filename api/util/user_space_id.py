from flask import request, abort, Response
from app import running_as_dev, socketio
from models import db
from models.in_space import InSpace
from uuid import UUID, uuid4
from base64 import b32decode, b32encode

# SameSite parameter for the SetCookie header. Should be strict if frontend and API run off one domain
samesite = "None" if running_as_dev else "Strict"

_cookies_user_id_key: str = "user_id"


def new_user_id() -> UUID:
    return uuid4()


def new_space_id() -> UUID:
    return uuid4()


def encode_space_id(space_id: UUID) -> str:
    return b32encode(space_id.bytes).decode()[0:-6].lower()


def decode_space_id(space_id: str) -> UUID:
    return UUID(bytes=b32decode(space_id.upper() + "======"))


def convert_to_response(resp):
    result = resp
    if isinstance(resp, tuple):
        result = Response(resp[0], status=resp[1])
    return result


def get_user_id():
    return (
        UUID(request.cookies[_cookies_user_id_key])
        if _cookies_user_id_key in request.cookies
        else None
    )


def with_user_id(func):
    def wrapped():
        set_cookie = False
        id = None
        if _cookies_user_id_key in request.cookies:
            try:
                id = get_user_id()
            except ValueError:
                abort(400)
        else:
            id = new_user_id()
            set_cookie = True

        res = convert_to_response(func(id))

        if set_cookie:
            res.set_cookie(
                _cookies_user_id_key, str(id), samesite=samesite, secure=True
            )

        return res

    wrapped.__name__ = func.__name__
    return wrapped


def space_member(user_id, space_id):
    return (
        db.session.execute(
            db.select(InSpace).filter(
                InSpace.space_id == space_id, InSpace.user_id == user_id
            )
        )
        .scalars()
        .one_or_none()
        is not None
    )


def with_space_id(func):
    def wrapped(user_id):
        space_id = user_id
        # A conservative method to detect if, on sucess, any state of the space might have been changed
        may_have_side_effects = request.method != "GET"
        is_concurrent = False
        args = dict(request.args)

        if "spid" in args:
            is_concurrent = True
            if not isinstance(args["spid"], str):
                abort(400)

            try:
                space_id = decode_space_id(args["spid"])
            except ValueError:
                abort(400)

            if not space_member(user_id=user_id, space_id=space_id):
                abort(403)

        res = convert_to_response(func(space_id))

        if 200 <= res.status_code < 300 and may_have_side_effects and is_concurrent:
            request_json = request.get_json(silent=False)
            # Some logic for excluding self
            excluded_sids = []
            if request_json is not None and "exclude_sid" in request_json:
                exclude_sid = request_json["exclude_sid"]
                if not isinstance(exclude_sid, str):
                    abort(400)
                # TODO: socket ID authorization?
                excluded_sids = [exclude_sid]

            socketio.emit(
                "space-update",
                {"id": args["spid"]},
                to=args["spid"],
                namespace="/spid",
                skip_sid=excluded_sids,
            )

        return res

    wrapped.__name__ = func.__name__
    return with_user_id(wrapped)
