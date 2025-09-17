import sys
import re
from collections import Counter

# =====================
# 文本归一化处理
# =====================
def normalize(text):
    """
    对输入文本进行归一化处理：
    - 去除标点和空格（仅保留中文、英文、数字）
    - 转为小写
    """
    text = re.sub(r'[^\w\u4e00-\u9fff]', '', text)  # 保留中文汉字和英文数字字母
    return text.lower().strip()

# =====================
# ngram分词与Dice系数模块
# =====================
def ngrams(s, n):
    """
    将字符串s按n个字符为一组切分，返回ngram列表
    """
    return [s[i:i+n] for i in range(max(0, len(s)-n+1))]

def dice_coefficient(a, b, n):
    """
    计算a和b的n-gram Dice相似度
    """
    A = ngrams(a, n)
    B = ngrams(b, n)
    if not A and not B:
        return 1.0
    cA = Counter(A)
    cB = Counter(B)
    inter = sum((cA & cB).values())
    return 2 * inter / (sum(cA.values()) + sum(cB.values()))

# =====================
# 编辑距离（Levenshtein Distance）模块
# =====================
def levenshtein(a, b):
    """
    计算字符串a和b的编辑距离（Levenshtein距离）
    """
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    prev = list(range(lb + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * lb
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            cur[j] = min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + cost)
        prev = cur
    return prev[lb]

# =====================
# 最长公共子序列（LCS）模块
# =====================
def lcs_len(a, b):
    """
    计算字符串a和b的最长公共子序列长度
    """
    la, lb = len(a), len(b)
    dp = [[0]*(lb+1) for _ in range(la+1)]
    for i in range(la-1, -1, -1):
        for j in range(lb-1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i+1][j+1]
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j+1])
    return dp[0][0]

# =====================
# 综合相似度计算模块
# =====================
def compute_similarity(a_raw, b_raw, weights=None):
    """
    综合计算两段文本的相似度，返回详细分数和中间结果：
    - ngram相似度
    - 编辑距离相似度
    - LCS相似度
    - 综合得分
    """
    a = normalize(a_raw)
    b = normalize(b_raw)
    # ngram相似度（字符级）
    sim1 = dice_coefficient(a, b, 1)
    sim2 = dice_coefficient(a, b, 2)
    sim3 = dice_coefficient(a, b, 3)
    sim_ngram = (sim1 + sim2 + sim3) / 3.0

    # 编辑距离相似度
    dist = levenshtein(a, b)
    maxlen = max(len(a), len(b))
    sim_edit = 1 - dist / maxlen if maxlen > 0 else 1.0

    # LCS相似度
    lcs = lcs_len(a, b)
    sim_lcs = lcs / maxlen if maxlen > 0 else 1.0

    # 默认权重
    if weights is None:
        weights = {'ngram': 0.45, 'edit': 0.25, 'lcs': 0.30}

    score = weights['ngram'] * sim_ngram + weights['edit'] * sim_edit + weights['lcs'] * sim_lcs
    return {
        'score': score,           # 综合得分
        'sim_ngram': sim_ngram,   # ngram相似度
        'sim_edit': sim_edit,     # 编辑距离相似度
        'sim_lcs': sim_lcs,       # LCS相似度
        'dist': dist,             # 编辑距离
        'lcs_len': lcs,           # LCS长度
        'len_a': len(a),          # 归一化后原文长度
        'len_b': len(b)           # 归一化后抄袭文长度
    }

# =====================
# 文件读取
# =====================
def read_file(path):
    """
    读取指定路径的文本文件内容
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# =====================
# 主程序入口
# =====================
if __name__ == '__main__':
    # 小测试，例句
    orig = "今天是星期天，天气晴，今天晚上我要去看电影。"
    plag = "今天是周天，天气晴朗，我晚上要去看电影。"
    res = compute_similarity(orig, plag)
    print("重复率(%) = {:.2f}".format(res['score']*100))
    print(res)