from collections import Counter

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
