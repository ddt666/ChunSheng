import requests
import os
import time

from setting import MUSIC_PATH
from setting import IMAGE_PATH
from setting import MONGO_DB

url = "https://m.ximalaya.com/mobile/v1/track/share/content?trackId=%s&tpName=weixin&device=h5"
content_list = ["/ertong/424529/7713660", "/ertong/424529/7713675",
                "/ertong/424529/7713577", "/ertong/424529/7713571",
                "/ertong/424529/7713546", "/ertong/424529/7713539"]


def xiaopapa(clist):
    my_content = []
    for i in clist:
        audio_id = i.rsplit("/", 1)[-1]
        print(audio_id)
        res = requests.get(url=url % (audio_id))

        res_dict = res.json()

        audioUrl = res_dict.get("audioUrl")
        picUrl = res_dict.get("picUrl")

        pic = requests.get(picUrl)
        audio = requests.get(audioUrl)
        from uuid import uuid4

        file_name = uuid4()
        image = os.path.join(IMAGE_PATH, f"{file_name}.jpg")
        music = os.path.join(MUSIC_PATH, f"{file_name}.mp3")

        # print(response.content)
        with open(music, "wb") as f:
            f.write(audio.content)

        with open(image, "wb") as cf:
            cf.write(pic.content)

        music_info = {
            "title": res_dict.get("title"),
            "nickname": res_dict.get("nickname"),
            "audio": f"{file_name}.mp3",
            "picUrl": f"{file_name}.jpg",
        }
        my_content.append(music_info)
        time.sleep(2)

    MONGO_DB.content.insert_many(my_content)

if __name__ == '__main__':
    xiaopapa(content_list)
