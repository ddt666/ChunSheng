import os

from aip import AipSpeech


""" 你的 APPID AK SK """
APP_ID = '17694171'
API_KEY = 'QHinaWpo1uUR485PHXwweARh'
SECRET_KEY = 'CfWxHu7Kif2latxQSn22NM6Fq0dNXaUp'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result  = client.synthesis('欢迎来到老男孩智能亲子互动乐园', 'zh', 1, {
    'vol': 5
})
path="Welcome.mp3"
with open(path,"wb") as f:
    f.write(result)


os.system(path)
