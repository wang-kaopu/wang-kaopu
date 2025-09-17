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

