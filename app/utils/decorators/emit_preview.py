from flask_socketio import emit

from app.socketio import rooms
from app.utils.rooms.decode_room import decode_room
from app.utils.rooms.prepare_preview import prepare_preview


def emit_preview(func):
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        [_, code] = res
        if not 200 <= code < 300:
            return res

        for room in rooms:
            room_data = decode_room(room)
            response = prepare_preview(room_data)
            emit('preview', response, to=room, namespace='/')

        return res

    inner.__name__ = func.__name__

    return inner
