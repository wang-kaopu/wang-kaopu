import re

def normalize(text):
    """
    对输入文本进行归一化处理：
    - 去除标点和空格（仅保留中文、英文、数字）
    - 转为小写
    """
    if text is None:
        return ""
    # 将标点符号替换为空格
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
    # 将多个空格合并为一个
    text = re.sub(r'\s+', ' ', text)
    # 转换为小写并去除首尾空格
    return text.lower().strip()
