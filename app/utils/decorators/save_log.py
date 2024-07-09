from typing import Callable

from flask import request, Response
from flask_jwt_extended import get_jwt_identity

from app.database import db
from app.models.log import Log


def save_log(func: Callable[..., tuple[Response, int]]):
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        [_, code] = res
        if 200 <= code < 300:
            data = request.get_json()
            keys = data.keys()
            message = func.__name__ + '('
            if len(keys) > 0:
                for key in keys:
                    message += f'{key}={data[key]},'
                message = message[:-1]
            message += ')'
            admin_id = get_jwt_identity()
            new_log = Log(admin_id=admin_id, message=message)
            db.session.add(new_log)
            db.session.commit()
        return res

    inner.__name__ = func.__name__

    return inner
