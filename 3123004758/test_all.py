import os
import subprocess

orig_dir = 'orig_lines'
plag_dir = 'plag_lines'
output_file = 'all_results.txt'
tmp_result = 'tmp_result.txt'

files = sorted([f for f in os.listdir(orig_dir) if f.endswith('.txt')], key=lambda x: int(os.path.splitext(x)[0]))

with open(output_file, 'w', encoding='utf-8') as out:
    for fname in files:
        orig_path = os.path.join(orig_dir, fname)
        plag_path = os.path.join(plag_dir, fname)
        # 调用main.py
        subprocess.run(['python', 'main.py', orig_path, plag_path, tmp_result], check=True)
        # 读取内容
        with open(orig_path, 'r', encoding='utf-8') as f:
            orig_content = f.read().strip()
        with open(plag_path, 'r', encoding='utf-8') as f:
            plag_content = f.read().strip()
        with open(tmp_result, 'r', encoding='utf-8') as f:
            result_content = f.read().strip()
        # 输出到总文件
        out.write('原文：\n')
        out.write(orig_content + '\n\n')
        out.write('抄袭：\n')
        out.write(plag_content + '\n\n')
        out.write('检测结果：\n')
        out.write(result_content + '\n')
        out.write('===============================\n\n')

if os.path.exists(tmp_result):
    os.remove(tmp_result)

print('全部处理完成，结果已输出到', output_file)
