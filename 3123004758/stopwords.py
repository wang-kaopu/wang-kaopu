STOPWORDS = set([
    "的", "了", "和", "是", "我", "你", "他", "她", "它", "在", "有", "也", "就", "不", "人", "都", "一个", "上", "中", "到", "说"
])

def is_all_stopwords(text):
    return all(char in STOPWORDS for char in text if char.strip())

def is_extreme_repeat(text):
    # 判断文本是否为单一字符极端重复
    return len(set(text)) == 1 and len(text) > 10
