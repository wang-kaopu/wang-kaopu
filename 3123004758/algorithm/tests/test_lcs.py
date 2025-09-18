import pytest
from ..lcs import lcs_len

def test_lcs_same_strings():
    """测试相同的字符串"""
    assert lcs_len("hello", "hello") == 5
    assert lcs_len("世界", "世界") == 2
    assert lcs_len("", "") == 0

def test_lcs_different_strings():
    """测试不同的字符串"""
    assert lcs_len("hello", "world") == 1  # 'o' is common
    assert lcs_len("测试", "验证") == 0
    assert lcs_len("ABCD", "ACBG") == 2  # 'AB' or 'AC' is common

def test_lcs_empty_strings():
    """测试空字符串"""
    assert lcs_len("hello", "") == 0
    assert lcs_len("", "world") == 0
    assert lcs_len("测试", "") == 0

def test_lcs_chinese_strings():
    """测试中文字符串"""
    assert lcs_len("你好世界", "你好世卫") == 3  # "你好世"
    assert lcs_len("中国人民", "中华人民") == 3  # "中人民"
    assert lcs_len("北京上海", "北京天津") == 2  # "北京"

def test_lcs_mixed_strings():
    """测试混合字符串"""
    assert lcs_len("hello世界", "hello世卫") == 6  # "hello世"
    assert lcs_len("test测试", "best测验") == 4  # "est测"

def test_lcs_subsequence():
    """测试子序列（不要求连续）"""
    assert lcs_len("ABCD", "ACBD") == 3  # "ABD" or "ACD"
    assert lcs_len("程序测试", "程序开发测试") == 4  # "程序测试"