import os

from flask import Blueprint, jsonify, send_file, request

from setting import MONGO_DB, RET, IMAGE_PATH, MUSIC_PATH

gsa = Blueprint("gsa", __name__)


@gsa.route('/get_image/<filename>')
def get_image(filename):
    file_path = os.path.join(IMAGE_PATH, filename)
    return send_file(file_path)


@gsa.route('/get_music/<filename>')
def get_music(filename):
    file_path = os.path.join(MUSIC_PATH, filename)
    return send_file(file_path)


@gsa.route('/uploader', methods=["post"])
def uploader():
    audio = request.files.get("recoder")
    audio.save(audio.filename)
    os.system(f"ffmpeg -i {audio.filename} {audio.filename}.mp3")
    return jsonify(RET)
