# 文本查重程序

这是一个基于多种算法的文本查重/相似度检测程序。该程序能够比较两段文本之间的相似度，适用于文本查重、抄袭检测等场景。

## 功能特点

- 支持多种文本相似度算法：
  - 编辑距离（Edit Distance）
  - 最长公共子序列（LCS）
  - N-gram 相似度
  - 余弦相似度
- 文本预处理：
  - 标准化处理
  - 停用词过滤
  - 文本规范化
- 支持命令行参数
- 生成详细的相似度分析报告

## 项目结构

```
.
├── algorithm/           # 算法模块目录
│   ├── edit_distance.py # 编辑距离算法
│   ├── lcs.py          # 最长公共子序列算法
│   ├── ngram.py        # N-gram相似度算法
│   ├── normalize.py    # 文本标准化处理
│   ├── similarity.py   # 相似度计算核心模块
│   └── stopwords.py    # 停用词处理
├── main.py             # 主程序入口
├── test_main.py        # 主程序测试
├── test_all.py         # 全局测试
└── requirements.txt    # 项目依赖
```

## 使用方法

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

1. 简单测试模式（使用内置示例）：
```bash
python main.py
```

2. 文件比较模式：
```bash
python main.py 原文文件路径 对比文件路径 输出文件路径
```

例如：
```bash
python main.py text/orig.txt text/orig_0.8_del.txt result.txt
```

## 输出结果

程序会生成一个结果文件，包含以下信息：
- 总体相似度得分（百分比）
- 各个算法的相似度详情
- 可能的重复/抄袭片段标注

## 性能分析

可以使用以下命令进行性能分析：
```bash
python -m cProfile -o result.prof main.py 原文文件路径 对比文件路径 输出文件路径
```

使用snakeviz查看性能分析结果：
```bash
snakeviz result.prof
```

## 测试

运行所有测试：
```bash
python test_all.py
```

运行主程序测试：
```bash
python test_main.py
```
