from flask import Blueprint, jsonify, request
from bson import ObjectId

from setting import MONGO_DB, RET

devices = Blueprint("devices", __name__)


@devices.route('/validate_code', methods=["post"])
def validate_code():
    code = request.form.to_dict()  # {device_key:0932rfwe938rw29}
    print(code)
    res = MONGO_DB.devices.find_one(code, {"_id": 0})
    if res:
        RET["code"] = 0
        RET["msg"] = "设备已授权，开启绑定"
        RET["data"] = res
    else:
        RET["code"] = 2
        RET["msg"] = "非授权设备"
        RET["data"] = {}

    return jsonify(RET)


@devices.route('/bind_toy', methods=["post"])
def bind_toy():
    toy_info = request.form.to_dict()
    # 好友之间聊天空间
    chat_window = MONGO_DB.chats.insert_one({"user_list": [], "chat_list": []})

    user_info = MONGO_DB.users.find_one({"_id": ObjectId(toy_info["user_id"])})
    print("toy_info", toy_info)
    toy_info["bind_user"] = toy_info.pop("user_id")
    toy_info["avatar"] = "toy.jpg"
    toy_info["friend_list"] = [
        {
            "friend_id": toy_info["bind_user"],
            "friend_name": user_info.get("nickname"),
            "friend_nick": toy_info.pop("remark"),
            "friend_avatar": user_info.get("avatar"),
            "friend_type": "app",
            "friend_chat": str(chat_window.inserted_id),

        }
    ]
    toy = MONGO_DB.toys.insert_one(toy_info)

    user_info["bind_toy"].append(str(toy.inserted_id))
    user_add_toy = {

        "friend_id": str(toy.inserted_id),
        "friend_name": toy_info.get("toy_name"),
        "friend_nick": toy_info.get("baby_name"),
        "friend_avatar": toy_info.get("avatar"),
        "friend_type": "toy",
        "friend_chat": str(chat_window.inserted_id),
    }

    user_info["friend_list"].append(user_add_toy)
    # user_info 整条修改
    MONGO_DB.users.update_one({"_id": ObjectId(user_info.get("_id"))}, {"$set": user_info})
    # 聊天窗口添加user_list
    MONGO_DB.chats.update_one({"_id": ObjectId(chat_window.inserted_id)}, {"$set": {"user_list": [
        str(toy.inserted_id), str(user_info.get("_id"))
    ]}})

    RET["code"] = 0
    RET["msg"] = "绑定好友成功"
    RET["data"] = {}

    return jsonify(RET)


@devices.route('/toy_list', methods=["post"])
def toy_list():
    user_id = request.form.get("user_id")

    user_info = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})

    user_bind_toys = user_info.get("bind_toy")  # ['5e05afd2c59a6b17a991b654','5e05afd2c59a6b17a991b654']

    toy_id_list = [ObjectId(toy) for toy in user_bind_toys]
    # print(toy_id_list)
    toy_l = list(MONGO_DB.toys.find({"_id": {"$in": toy_id_list}}))
    for toy in toy_l:
        toy["_id"] = str(toy.get("_id"))

    RET["code"] = 0
    RET["msg"] = "查找所有玩具列表"
    RET["data"] = toy_l
    return jsonify(RET)
