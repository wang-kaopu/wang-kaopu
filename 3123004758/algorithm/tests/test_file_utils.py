import pytest
import os
import tempfile
from ..file_utils import read_file

def test_read_file_normal():
    """测试正常文件读取"""
    # 创建临时文件进行测试
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        content = "这是测试文本\n包含多行内容\n测试UTF-8编码"
        f.write(content)
        temp_path = f.name

    try:
        # 读取文件
        result = read_file(temp_path)
        assert result == "这是测试文本 包含多行内容 测试UTF-8编码"
    finally:
        # 清理临时文件
        os.remove(temp_path)

def test_read_file_empty():
    """测试空文件读取"""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        temp_path = f.name

    try:
        result = read_file(temp_path)
        assert result == ""
    finally:
        os.remove(temp_path)

def test_read_file_not_exists():
    """测试不存在的文件"""
    with pytest.raises(FileNotFoundError):
        read_file("not_exists_file.txt")

def test_read_file_with_spaces():
    """测试包含多个空格的文件"""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        content = "多个    空格   测试\n  缩进  测试  "
        f.write(content)
        temp_path = f.name

    try:
        result = read_file(temp_path)
        assert result == "多个 空格 测试 缩进 测试"
    finally:
        os.remove(temp_path)

def test_read_file_special_chars():
    """测试包含特殊字符的文件"""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        content = "特殊符号!@#$%^&*\n换行符\t制表符"
        f.write(content)
        temp_path = f.name

    try:
        result = read_file(temp_path)
        assert "特殊符号" in result
        assert "换行符" in result
        assert "制表符" in result
    finally:
        os.remove(temp_path)