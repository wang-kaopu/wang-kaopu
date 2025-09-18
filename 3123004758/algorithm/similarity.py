import math
import numpy as np
from .ngram import dice_coefficient
from .edit_distance import levenshtein
from .lcs import lcs_len
from .normalize import normalize
from .stopwords import is_all_stopwords, is_extreme_repeat

def cosine_similarity(a, b):
    """计算两个向量的余弦相似度
    
    Args:
        a: 第一个向量（列表形式）
        b: 第二个向量（列表形式）
        
    Returns:
        float: 余弦相似度值，范围[0, 1]
    """
    # 处理空向量
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
        
    from collections import Counter
    vec_a = Counter(a)
    vec_b = Counter(b)
    
    # 获取所有唯一键
    all_keys = sorted(set(vec_a.keys()) | set(vec_b.keys()))
    
    # 向量化计算（使用numpy.float64以提高精度）
    vec_a_array = np.array([vec_a.get(k, 0) for k in all_keys], dtype=np.float64)
    vec_b_array = np.array([vec_b.get(k, 0) for k in all_keys], dtype=np.float64)
    
    # 计算点积和范数
    dot_product = float(np.dot(vec_a_array, vec_b_array))
    norm_a = float(np.linalg.norm(vec_a_array))
    norm_b = float(np.linalg.norm(vec_b_array))
    
    # 处理零向量
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
        
    # 计算相似度并确保结果在[0,1]范围内
    similarity = dot_product / (norm_a * norm_b)
    if abs(similarity) < 1e-10:  # 处理接近于0的情况
        return 0.0
    return min(1.0, max(0.0, similarity))

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

def compute_similarity(a_raw, b_raw, weights=None, threshold=200):
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
    
    # 向量化计算ngram相似度
    sim1 = dice_coefficient(a, b, 1)
    sim2 = dice_coefficient(a, b, 2)
    sim3 = dice_coefficient(a, b, 3)
    sim_ngram = (sim1 + sim2 + sim3) / 3.0
    
    # 余弦相似度（已向量化）
    sim_cosine = cosine_similarity(a, b)
    # Jaccard系数
    sim_jaccard = jaccard_similarity(a, b)
    
    # 短文本：全算法
    if max(len(a), len(b)) <= threshold:
        dist = levenshtein(a, b)
        maxlen = max(len(a), len(b))
        sim_edit = 1 - dist / maxlen if maxlen > 0 else 1.0
        lcs = lcs_len(a, b)
        sim_lcs = lcs / maxlen if maxlen > 0 else 1.0
        # 默认权重
        if weights is None:
            weights = {'ngram': 0.45, 'edit': 0.25, 'lcs': 0.30}
        # 向量化权重计算
        weight_array = np.array([weights['ngram'], weights['edit'], weights['lcs']])
        sim_array = np.array([sim_ngram, sim_edit, sim_lcs])
        score = np.dot(weight_array, sim_array)
        return {
            'score': float(score),        # 综合得分
            'sim_ngram': sim_ngram,       # ngram相似度
            'sim_edit': sim_edit,         # 编辑距离相似度
            'sim_lcs': sim_lcs,           # LCS相似度
            'sim_cosine': sim_cosine,     # 余弦相似度
            'sim_jaccard': sim_jaccard,   # Jaccard系数
            'dist': dist,                 # 编辑距离
            'lcs_len': lcs,               # LCS长度
            'len_a': len(a),              # 归一化后原文长度
            'len_b': len(b),              # 归一化后抄袭文长度
            'mode': 'short'               # 短文本模式
        }
    # 长文本：只用高效算法
    else:
        # 默认权重（长文本）
        if weights is None:
            weights = {'ngram': 0.5, 'cosine': 0.3, 'jaccard': 0.2}
        # 向量化权重计算
        weight_array = np.array([weights['ngram'], weights['cosine'], weights['jaccard']])
        sim_array = np.array([sim_ngram, sim_cosine, sim_jaccard])
        score = np.dot(weight_array, sim_array)
        return {
            'score': float(score),        # 综合得分
            'sim_ngram': sim_ngram,       # ngram相似度
            'sim_edit': None,             # 编辑距离相似度（长文本不计算）
            'sim_lcs': None,              # LCS相似度（长文本不计算）
            'sim_cosine': sim_cosine,     # 余弦相似度
            'sim_jaccard': sim_jaccard,   # Jaccard系数
            'dist': None,                 # 编辑距离（长文本不计算）
            'lcs_len': None,              # LCS长度（长文本不计算）
            'len_a': len(a),              # 归一化后原文长度
            'len_b': len(b),              # 归一化后抄袭文长度
            'mode': 'long'                # 长文本模式
        }

def batch_compute_similarity(text_pairs, weights=None, threshold=200):
    """
    批量计算相似度，使用NumPy向量化处理
    """
    results = []
    for a_raw, b_raw in text_pairs:
        result = compute_similarity(a_raw, b_raw, weights, threshold)
        results.append(result)
    return results