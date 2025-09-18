import re

def normalize(text):
    """
    对输入文本进行归一化处理：
    - 去除标点和空格（仅保留中文、英文、数字）
    - 转为小写
    """
    text = re.sub(r'[^-\u007f\w\u4e00-\u9fff]', '', text)
    return text.lower().strip()
