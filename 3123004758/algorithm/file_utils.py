import os

def ensure_dir(path):
    """
    确保目录存在，如果不存在则创建
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def write_file(path, content):
    """
    写入文本内容到指定路径的文件，自动创建目录
    """
    try:
        ensure_dir(path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"写入文件时发生错误: {path}，错误信息: {e}")
        return False

def read_file(path):
    """
    读取指定路径的文本文件内容，自动处理文件不存在和编码问题
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"文件不存在: {path}")
        return ""
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='gbk') as f:
                return f.read()
        except Exception as e:
            print(f"文件编码错误且无法自动识别: {path}，错误信息: {e}")
            return ""
    except Exception as e:
        print(f"读取文件时发生未知错误: {path}，错误信息: {e}")
        return ""
