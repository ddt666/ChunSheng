from flask import Blueprint, jsonify, request
from bson import ObjectId

from setting import MONGO_DB, RET

friend = Blueprint("friend", __name__)


@friend.route('/friend_list', methods=["post"])
def friend_list():
    user_id = request.form.get("user_id")

    user_info = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})

    RET["code"] = 0
    RET["msg"] = "获取好友列表"
    RET["data"] = user_info.get("friend_list")

    return jsonify(RET)
