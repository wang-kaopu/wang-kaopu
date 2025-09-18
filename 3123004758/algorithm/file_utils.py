def read_file(path):
    """
    读取指定路径的文本文件内容，自动处理文件不存在和编码问题
    规范化文本内容，将连续空白字符替换为单个空格
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 将多个空格、制表符、换行符替换为单个空格
            return ' '.join(content.split())
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {path}")
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
