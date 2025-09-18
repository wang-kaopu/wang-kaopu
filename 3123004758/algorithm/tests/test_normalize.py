import pytest
from ..normalize import normalize

def test_normalize_basic():
    """测试基本的文本规范化"""
    assert normalize("Hello World!") == "hello world"
    assert normalize("测试Text") == "测试text"
    assert normalize("   空格测试   ") == "空格测试"

def test_normalize_punctuation():
    """测试标点符号处理"""
    assert normalize("Hello, World!") == "hello world"
    assert normalize("测试。文本！") == "测试文本"
    assert normalize("semi;colon:test") == "semicolontest"

def test_normalize_whitespace():
    """测试空白字符处理"""
    assert normalize("multiple    spaces") == "multiple spaces"
    assert normalize("\t制表符\n换行") == "制表符换行"
    assert normalize(" leading trailing ") == "leading trailing"

def test_normalize_mixed_text():
    """测试混合文本"""
    assert normalize("Hello世界！") == "hello世界"
    assert normalize("TEST测试。123") == "test测试123"
    assert normalize("中文,English,123") == "中文english123"

def test_normalize_numbers():
    """测试数字处理"""
    assert normalize("123") == "123"
    assert normalize("test123") == "test123"
    assert normalize("123test") == "123test"

def test_normalize_special_cases():
    """测试特殊情况"""
    assert normalize("") == ""
    assert normalize(" ") == ""
    assert normalize("!!!") == ""
    assert normalize("...") == ""