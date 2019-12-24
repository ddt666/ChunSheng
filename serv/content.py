from flask import Blueprint, jsonify

from setting import MONGO_DB
from setting import RET

content = Blueprint("content", __name__)


@content.route('/content_list',methods=["post"])
def content_list():
    res = list(MONGO_DB.content.find({}))
    for index, item in enumerate(res):
        res[index]["_id"] = str(item.get("_id"))
    RET["code"] = 0
    RET["msg"] = "查询幼教内容"
    RET["data"] = res
    return jsonify(RET)
