import sys
from file_utils import read_file
from similarity import compute_similarity

if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            # 小测试，例句
            orig = "今天是星期天，天气晴，今天晚上我要去看电影。"
            plag = "今天是周天，天气晴朗，我晚上要去看电影。"
            res = compute_similarity(orig, plag)
            print("重复率(%) = {:.2f}".format(res['score']*100))
            print(res)
        elif len(sys.argv) == 4:
            # 命令行参数模式：原文、抄袭文、输出文件
            orig_path = sys.argv[1]
            plag_path = sys.argv[2]
            out_path = sys.argv[3]
            orig = read_file(orig_path)
            plag = read_file(plag_path)
            res = compute_similarity(orig, plag)
            if 'error' in res:
                print("检测异常：", res['error'])
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write("检测异常：{}\n".format(res['error']))
            else:
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write("重复率(%) = {:.2f}\n".format(res['score']*100))
                    f.write(str(res) + "\n")
        else:
            print("用法: python main.py 原文路径 抄袭版路径 答案输出路径")
    except Exception as e:
        print("程序运行时发生异常：", e)