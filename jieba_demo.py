import jieba

res = list(jieba.cut_for_search("白日依山尽，黄河入海流"))
print("res执行了")
print(res)