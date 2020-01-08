import json

from flask import Flask, request, jsonify
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket
from bson import ObjectId

from ai.baidu import text2audio,_get_xxtx
from redismsg import set_redis
from setting import MONGO_DB, RET

ws_app = Flask(__name__)

user_socket_dict = {}


@ws_app.route("/app/<app_id>")
def app(app_id):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[app_id] = user_socket
    print(user_socket_dict)
    while 1:
        try:
            user_msg = user_socket.receive()
            print("app_user_msg",
                  user_msg)  # {to_user:"toy_id",chat:"xxxx.mp3",from_user:"sadasfasfasf0932d2ehdqadgkjh"}
            if user_msg:
                msg_dict = json.loads(user_msg)
                from_user = msg_dict.get("from_user")
                to_user = msg_dict.get("to_user")
                msg_dict["chat"] = _get_xxtx(to_user, from_user)
                toy_socket = user_socket_dict.get(to_user)
                set_redis(to_user, from_user)
                msg_dict["friend_type"] = "app"
                toy_socket.send(json.dumps(msg_dict))
        except:

            RET["code"] = 0
            RET["msg"] = "websocket已断开"
            RET["data"] = {}
            return jsonify(RET)


@ws_app.route("/toy/<toy_id>")
def toy(toy_id):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[toy_id] = user_socket
    print(user_socket_dict)
    while 1:
        try:
            user_msg = user_socket.receive()
            print("toy_user_msg", user_msg)
            if user_msg:
                msg_dict = json.loads(user_msg)
                from_user = msg_dict.get("from_user")
                to_user = msg_dict.get("to_user")
                if msg_dict.get("friend_type") == "toy":
                    msg_dict["chat"] = _get_xxtx(to_user, from_user)
                toy_socket = user_socket_dict.get(to_user)
                set_redis(to_user, from_user)
                print("msg_dict", msg_dict)
                msg_dict["friend_type"] = "toy"
                toy_socket.send(json.dumps(msg_dict))
        except:
            # 前端的ws.onerror事件接收返回值
            RET["code"] = 0
            RET["msg"] = "websocket已断开"
            RET["data"] = {}
            return jsonify(RET)




if __name__ == '__main__':
    http_serv = WSGIServer(("0.0.0.0", 3721), ws_app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
