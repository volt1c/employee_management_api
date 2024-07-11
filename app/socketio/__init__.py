# pylint: disable=possibly-used-before-assignment
from flask import request
from flask_socketio import SocketIO, join_room, emit

from app.utils.rooms.encode_room import encode_room

socketio = SocketIO()

if 'rooms' not in locals():
    rooms = {}


@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    for room in rooms.items():
        if sid in room:
            room.remove(sid)


@socketio.on('join')
def on_join_preview(data):
    if not data:
        return

    room = encode_room(data)
    join_room(room)
    sid = request.sid

    if room in rooms:
        if sid in rooms[room]:
            emit('message', {
                'message': 'You are already connected to this preview.'
            }, to=sid)
            return
        rooms[room].append(sid)
    else:
        rooms[room] = [sid]

    emit('message', {
        'message': 'New device connected. 🔌'
    }, skip_sid=sid)
    emit('message', {
        'message': 'Connected successfully. 🔌'
    }, to=sid)
