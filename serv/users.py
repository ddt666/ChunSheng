from flask import Blueprint, jsonify, request

from setting import MONGO_DB
from setting import RET

users = Blueprint("users", __name__)


@users.route('/reg', methods=["post"])
def reg():
    user_info = request.form.to_dict()
    user_info["avatar"] = "mama.jpg" if user_info.get("gender") == "1" else "baba.jpg"
    user_info["friend_list"] = []
    user_info["bind_toy"] = []
    res = MONGO_DB.users.insert_one(user_info)
    RET["code"] = 0
    RET["msg"] = "用户注册成功"
    RET["data"] = {"user_id": str(res.inserted_id)}

    return jsonify(RET)


@users.route('/login', methods=["post"])
def login():
    user = request.form.to_dict()
    # print(user)
    user = MONGO_DB.users.find_one(user, {"password": 0})
    if user:
        RET["code"] = 0
        RET["msg"] = "登录成功"
        user["_id"] = str(user.get("_id"))
        RET["data"] = user
    else:
        RET["code"] = -1
        RET["msg"] = "用户名密码错误"

    return jsonify(RET)
