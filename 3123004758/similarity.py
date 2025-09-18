import math
from ngram import dice_coefficient
from edit_distance import levenshtein
from lcs import lcs_len
from normalize import normalize
from stopwords import is_all_stopwords, is_extreme_repeat

def cosine_similarity(a, b):
    from collections import Counter
    vec_a = Counter(a)
    vec_b = Counter(b)
    all_keys = set(vec_a.keys()) | set(vec_b.keys())
    dot = sum(vec_a[k] * vec_b[k] for k in all_keys)
    norm_a = math.sqrt(sum(v*v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v*v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def jaccard_similarity(a, b):
    set_a = set(a)
    set_b = set(b)
    if not set_a and not set_b:
        return 1.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    if union == 0:
        return 0.0
    return inter / union

def compute_similarity(a_raw, b_raw, weights=None):
    a = normalize(a_raw)
    b = normalize(b_raw)
    # 空文本
    if not a or not b:
        return {'score': 0.0, 'error': '输入文本为空'}
    # 全为停用词
    if is_all_stopwords(a) or is_all_stopwords(b):
        return {'score': 0.0, 'error': '文本全为停用词'}
    # 极端重复
    if is_extreme_repeat(a) or is_extreme_repeat(b):
        return {'score': 0.0, 'error': '文本极端重复'}
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
    # 余弦相似度
    sim_cosine = cosine_similarity(a, b)
    # Jaccard系数
    sim_jaccard = jaccard_similarity(a, b)
    # 默认权重
    if weights is None:
        weights = {'ngram': 0.45, 'edit': 0.25, 'lcs': 0.30}
    score = weights['ngram'] * sim_ngram + weights['edit'] * sim_edit + weights['lcs'] * sim_lcs
    return {
        'score': score,           # 综合得分
        'sim_ngram': sim_ngram,   # ngram相似度
        'sim_edit': sim_edit,     # 编辑距离相似度
        'sim_lcs': sim_lcs,       # LCS相似度
        'sim_cosine': sim_cosine, # 余弦相似度
        'sim_jaccard': sim_jaccard, # Jaccard系数
        'dist': dist,             # 编辑距离
        'lcs_len': lcs,           # LCS长度
        'len_a': len(a),          # 归一化后原文长度
        'len_b': len(b)           # 归一化后抄袭文长度
    }
