import requests
import uuid
import time
import hashlib
import os

from setting import LT_URL, QRCODE_PATH, MONGO_DB


def create_QR(count):
    qr_list = []
    for i in range(count):
        QR_code = hashlib.md5(f"{uuid.uuid4()}{time.time()}{uuid.uuid4()}".encode("utf8")).hexdigest()

        res = requests.get(LT_URL % QR_code)

        path = os.path.join(QRCODE_PATH, f"{QR_code}.jpg")
        with open(path, "wb") as f:
            f.write(res.content)
        qr_dict = {"device_key": QR_code}
        qr_list.append(qr_dict)
        time.sleep(2)

    MONGO_DB.devices.insert_many(qr_list)


if __name__ == '__main__':
    create_QR(10)
