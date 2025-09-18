import pytest
from ..stopwords import is_all_stopwords, is_extreme_repeat

def test_is_all_stopwords():
    """测试停用词检查"""
    # 常见停用词
    assert is_all_stopwords("的") == True
    assert is_all_stopwords("了") == True
    assert is_all_stopwords("的了") == True
    
    # 非停用词
    assert is_all_stopwords("测试") == False
    assert is_all_stopwords("python") == False
    
    # 混合情况
    assert is_all_stopwords("的测试") == False
    assert is_all_stopwords("python的") == False

def test_is_all_stopwords_edge_cases():
    """测试停用词检查的边界情况"""
    # 空字符串
    assert is_all_stopwords("") == False
    
    # 空格
    assert is_all_stopwords(" ") == False
    assert is_all_stopwords("的 了") == True
    
    # 标点符号
    assert is_all_stopwords("，") == False
    assert is_all_stopwords("的，了") == True

def test_is_extreme_repeat():
    """测试极端重复检查"""
    # 重复文本
    assert is_extreme_repeat("测试测试测试测试") == True
    assert is_extreme_repeat("aaaaaa") == True
    
    # 非重复文本
    assert is_extreme_repeat("这是一个测试") == False
    assert is_extreme_repeat("hello world") == False
    
    # 部分重复
    assert is_extreme_repeat("测试测试，验证") == False
    assert is_extreme_repeat("test test test code") == False

def test_is_extreme_repeat_edge_cases():
    """测试极端重复检查的边界情况"""
    # 空字符串
    assert is_extreme_repeat("") == False
    
    # 单个字符
    assert is_extreme_repeat("a") == False
    assert is_extreme_repeat("测") == False
    
    # 空格和标点
    assert is_extreme_repeat("   ") == True
    assert is_extreme_repeat("...") == True
    
    # 混合重复
    assert is_extreme_repeat("test测试test测试") == True