import os

from flask import Blueprint, jsonify, send_file

from setting import MONGO_DB, RET, IMAGE_PATH,MUSIC_PATH

gsa = Blueprint("gsa", __name__)


@gsa.route('/get_image/<filename>')
def get_image(filename):
    file_path = os.path.join(IMAGE_PATH, filename)
    return send_file(file_path)


@gsa.route('/get_music/<filename>')
def get_music(filename):
    file_path = os.path.join(MUSIC_PATH, filename)
    return send_file(file_path)
