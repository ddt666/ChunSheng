from pypinyin import lazy_pinyin,TONE2

res =lazy_pinyin("先帝创业未半而中道奔殂",style=TONE2)

print(res)