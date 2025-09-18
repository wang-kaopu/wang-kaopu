import pytest
import numpy as np
from ..similarity import (
    compute_similarity,
    cosine_similarity,
    jaccard_similarity
)

def test_cosine_similarity():
    """测试余弦相似度计算"""
    # 相同向量
    assert cosine_similarity([1, 1], [1, 1]) == pytest.approx(1.0)
    # 正交向量
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)
    # 一般情况
    assert 0 <= cosine_similarity([1, 2], [2, 3]) <= 1
    # 零向量
    assert cosine_similarity([0, 0], [1, 1]) == 0.0

def test_jaccard_similarity():
    """测试Jaccard相似度计算"""
    # 相同集合
    assert jaccard_similarity({1, 2, 3}, {1, 2, 3}) == 1.0
    # 不相交集合
    assert jaccard_similarity({1, 2}, {3, 4}) == 0.0
    # 部分重叠
    assert jaccard_similarity({1, 2, 3}, {2, 3, 4}) == pytest.approx(0.5)
    # 空集
    assert jaccard_similarity(set(), {1, 2}) == 0.0
    assert jaccard_similarity(set(), set()) == 1.0

def test_jaccard_similarity():
    """测试Jaccard相似度计算"""
    # 相同集合
    assert jaccard_similarity({1, 2, 3}, {1, 2, 3}) == 1.0
    # 不相交集合
    assert jaccard_similarity({1, 2}, {3, 4}) == 0.0
    # 部分重叠
    assert jaccard_similarity({1, 2, 3}, {2, 3, 4}) == pytest.approx(0.5)

def test_compute_similarity_valid_input():
    """测试整体相似度计算-有效输入"""
    # 相同文本
    result = compute_similarity("测试文本", "测试文本")
    assert result['score'] == pytest.approx(1.0)
    assert 'error' not in result
    
    # 部分相似文本
    result = compute_similarity("今天天气真好", "今天天气不错")
    assert 0 <= result['score'] <= 1
    assert 'error' not in result

def test_compute_similarity_empty_input():
    """测试整体相似度计算-空输入"""
    # 空字符串
    result = compute_similarity("", "")
    assert 'error' in result
    
    # None输入
    result = compute_similarity(None, "测试")
    assert 'error' in result

def test_compute_similarity_edge_cases():
    """测试整体相似度计算-边界情况"""
    # 非常长的文本
    long_text = "测试" * 1000
    result = compute_similarity(long_text, long_text)
    assert 0 <= result['score'] <= 1
    
    # 包含特殊字符
    result = compute_similarity("测试!@#$%", "测试!@#$%")
    assert 0 <= result['score'] <= 1