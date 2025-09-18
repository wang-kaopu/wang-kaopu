import pytest
import os
import tempfile
from ..file_utils import read_file, write_file, ensure_dir

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

def test_write_file_normal():
    """测试正常写入文件"""
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "test.txt")
    
    try:
        content = "测试写入内容\n包含换行"
        write_file(file_path, content)
        
        # 验证写入的内容
        with open(file_path, 'r', encoding='utf-8') as f:
            written_content = f.read()
        assert written_content == content
    finally:
        # 清理
        if os.path.exists(file_path):
            os.remove(file_path)
        os.rmdir(temp_dir)

def test_ensure_dir_normal():
    """测试正常创建目录"""
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "newdir")
    
    try:
        ensure_dir(new_dir)
        assert os.path.exists(new_dir)
        assert os.path.isdir(new_dir)
    finally:
        if os.path.exists(new_dir):
            os.rmdir(new_dir)
        os.rmdir(temp_dir)

def test_read_file_permission_denied():
    """测试读取权限被拒绝的文件"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        temp_path = f.name
    
    try:
        # Windows下设置为只写
        os.chmod(temp_path, 0o200)
        with pytest.raises(PermissionError) as exc_info:
            read_file(temp_path)
        assert "没有权限读取文件" in str(exc_info.value)
    finally:
        os.chmod(temp_path, 0o666)
        os.remove(temp_path)

def test_write_file_permission_denied():
    """测试写入权限被拒绝"""
    temp_dir = tempfile.mkdtemp()
    try:
        # 设置目录为只读
        os.chmod(temp_dir, 0o444)
        file_path = os.path.join(temp_dir, "test.txt")
        
        with pytest.raises(PermissionError) as exc_info:
            write_file(file_path, "测试内容")
        assert "没有权限写入文件" in str(exc_info.value)
    finally:
        # 恢复权限以便清理
        os.chmod(temp_dir, 0o777)
        os.rmdir(temp_dir)

def test_ensure_dir_permission_denied():
    """测试创建目录权限被拒绝"""
    temp_dir = tempfile.mkdtemp()
    try:
        os.chmod(temp_dir, 0o444)  # 设置为只读
        new_dir = os.path.join(temp_dir, "newdir")
        
        with pytest.raises(PermissionError) as exc_info:
            ensure_dir(new_dir)
        assert "没有权限创建目录" in str(exc_info.value)
    finally:
        os.chmod(temp_dir, 0o777)  # 恢复权限以便清理
        os.rmdir(temp_dir)

def test_read_file_encoding_error():
    """测试文件编码错误"""
    # 创建一个无效UTF-8编码的文件
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b'\xFF\xFE\xFA')  # 无效的UTF-8字节
        temp_path = f.name
    
    try:
        with pytest.raises(UnicodeDecodeError) as exc_info:
            read_file(temp_path)
        assert "文件编码错误" in str(exc_info.value)
    finally:
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