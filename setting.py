# 目录配置

import os

MUSIC_PATH = "Music"
IMAGE_PATH = "Image"
QRCODE_PATH = "QRcode"

# 数据库配置

import pymongo

client = pymongo.MongoClient(host="127.0.0.1", port=27017)
MONGO_DB = client["chunsheng"]

# rest-api
RET = {
    "code": 0,
    "msg": "",
    "data": {}
}

# 联图配置
LT_URL = "http://qr.liantu.com/api.php?text=%s"
