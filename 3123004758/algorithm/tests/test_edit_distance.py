import pytest
from ..edit_distance import levenshtein

def test_levenshtein_same_strings():
    """测试两个相同的字符串"""
    assert levenshtein("hello", "hello") == 0
    assert levenshtein("世界", "世界") == 0
    assert levenshtein("", "") == 0

def test_levenshtein_different_strings():
    """测试两个不同的字符串"""
    assert levenshtein("hello", "world") == 4
    assert levenshtein("世界", "世卫") == 1
    assert levenshtein("测试", "测验") == 1

def test_levenshtein_empty_strings():
    """测试空字符串情况"""
    assert levenshtein("hello", "") == 5
    assert levenshtein("", "world") == 5
    assert levenshtein("测试", "") == 2

def test_levenshtein_chinese_strings():
    """测试中文字符串"""
    assert levenshtein("你好世界", "你好世卫") == 1
    assert levenshtein("中国人", "中华人") == 1
    assert levenshtein("北京市", "南京市") == 1

def test_levenshtein_mixed_strings():
    """测试混合字符串"""
    assert levenshtein("hello世界", "hello世卫") == 1
    assert levenshtein("test测试", "test测验") == 1