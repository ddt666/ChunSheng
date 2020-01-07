import json

from flask import Flask, request
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket
from bson import ObjectId

from ai.baidu import text2audio
from redismsg import set_redis
from setting import MONGO_DB


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
        print(user_msg)  # {to_user:"toy_id",chat:"xxxx.mp3",from_user:"sadasfasfasf0932d2ehdqadgkjh"}
        if user_msg:

            msg_dict = json.loads(user_msg)
            from_user = msg_dict.get("from_user")
            to_user = msg_dict.get("to_user")
            msg_dict["chat"] = _get_xxtx(to_user, from_user)
            toy_socket = user_socket_dict.get(to_user)
            set_redis(to_user, from_user)
            toy_socket.send(json.dumps(msg_dict))



@ws_app.route("/toy/<toy_id>")
def toy(toy_id):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[toy_id] = user_socket
    print(user_socket_dict)
    while 1:
        user_msg = user_socket.receive()
        print(user_msg)
        if user_msg:
            msg_dict = json.loads(user_msg)
            from_user = msg_dict.get("from_user")
            to_user = msg_dict.get("to_user")
            toy_socket = user_socket_dict.get(to_user)
            set_redis(to_user, from_user)
            toy_socket.send(user_msg)



def _get_xxtx(to_user, from_user):
    toy = MONGO_DB.toys.find_one({"_id": ObjectId(to_user)})
    friend_list = toy.get("friend_list")
    xxtx_str = "你有来自陌生人的消息"
    for f in friend_list:
        if f.get("friend_id") == from_user:
            xxtx_str = f"你有来自{f.get('friend_nick')}的消息"
            break
    filename = text2audio(xxtx_str)
    return filename


if __name__ == '__main__':
    http_serv = WSGIServer(("0.0.0.0", 3721), ws_app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
