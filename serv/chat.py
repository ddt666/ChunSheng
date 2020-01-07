import os
from uuid import uuid4
import time

from flask import Blueprint, jsonify, send_file, request

from setting import MONGO_DB, RET, IMAGE_PATH, MUSIC_PATH, CHATS_PATH
from redismsg import get_reids_one,get_reids_all

chat = Blueprint("chat", __name__)


@chat.route('/recv_msg', methods=["post"])
def get_msg():
    from_user = request.form.get("from_user")
    to_user = request.form.get("to_user")
    count = get_reids_one(to_user, from_user)
    print("count", count)
    chat_window = MONGO_DB.chats.find_one({"user_list": {"$all": [from_user, to_user]}})
    chat_list = []
    if count:

        # reversed 函数返回一个反转的迭代器
        for chat in reversed(chat_window.get("chat_list")):
            if chat.get("sender") != from_user:
                continue
            if len(chat_list) == count:
                break
            chat_list.append(chat)

        # reverse() 函数用于反向列表中元素。
        chat_list.reverse()
    print("chat_list", chat_list)
    return jsonify(chat_list)


@chat.route('/chat_list', methods=["post"])
def chat_list():
    from_user = request.form.get("from_user")
    to_user = request.form.get("to_user")
    print("chat_list",from_user,to_user)
    chat_window = MONGO_DB.chats.find_one({"user_list": {"$all": [from_user, to_user]}})
    get_reids_one(to_user,from_user)
    RET["code"] = 0
    RET["msg"] = "获取消息列表"
    RET["data"] = chat_window.get("chat_list")[-10:]

    return jsonify(RET)


@chat.route('/chat_count', methods=["post"])
def chat_count():
    user_id = request.form.get("user_id")
    to_user_msg = get_reids_all(user_id)

    RET["code"] = 0
    RET["msg"] = "查询未读消息"
    RET["data"] = to_user_msg
    return jsonify(RET)