import json

from flask import Flask, request
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket

ws_app = Flask(__name__)

user_socket_dict = {}


@ws_app.route("/app/<app_id>")
def app(app_id):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[app_id] = user_socket
    print(user_socket_dict)
    while 1:
        user_msg = user_socket.receive()
        print(user_msg)  # {to_user:"toy_id",music:"xxxx.mp3"}
        if user_msg:
            msg_dict = json.loads(user_msg)
            toy_socket = user_socket_dict.get(msg_dict.get("to_user"))
            toy_socket.send(user_msg)


@ws_app.route("/toy/<toy_id>")
def toy(toy_id):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[toy_id] = user_socket
    print(user_socket_dict)
    while 1:
        user_msg = user_socket.receive()
        print(user_msg)


if __name__ == '__main__':
    http_serv = WSGIServer(("0.0.0.0", 3721), ws_app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
