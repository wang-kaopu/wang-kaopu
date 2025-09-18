STOPWORDS = set([
    "的", "了", "和", "是", "我", "你", "他", "她", "它", "在", "有", "也", "就", "不", "人", "都", "一个", "上", "中", "到", "说"
])

def is_all_stopwords(text):
    """判断文本是否全部由停用词组成"""
    if not text:
        return False
    
    # 将标点符号替换为空格，然后分词
    text = ''.join(char if char.isalnum() or char.isspace() else ' ' for char in text)
    words = [word for word in text.split() if word.strip()]
    
    if not words:
        return False
        
    return all(word in STOPWORDS for word in words)

def is_extreme_repeat(text):
    """判断文本是否存在极端重复
    
    判断标准：
    1. 全是空白字符
    2. 单一字符重复超过3次
    3. 同一词语重复超过3次且占比超过50%
    """
    if not text:
        return False
    
    # 处理纯空白字符
    if text.isspace():
        return True
    
    # 清理文本，去除空白字符
    clean_text = ''.join(text.split())
    if not clean_text:
        return False
    
    # 检查单一字符重复
    if len(set(clean_text)) == 1:
        return True
    
    # 分词并统计
    words = [w for w in text.split() if w.strip()]
    if not words:
        return False
    
    word_count = {}
    max_count = 0
    total_words = len(words)
    
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
        max_count = max(max_count, word_count[word])
    
    # 判断重复词的比例
    return max_count >= 3 and max_count / total_words > 0.5
