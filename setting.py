# 目录配置

import os

MUSIC_PATH = "Music"
IMAGE_PATH = "Image"

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
