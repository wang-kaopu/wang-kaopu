import main

def test_normalize():
    assert main.normalize('Hello, 世界! 123') == 'hello世界123'

def test_ngrams():
    assert main.ngrams('abcd', 2) == ['ab', 'bc', 'cd']

def test_dice_coefficient():
    a = 'abcd'
    b = 'abef'
    # 2-gram: ab, bc, cd vs ab, be, ef
    # 交集: ab
    # 总数: 3+3=6
    # dice = 2*1/6 = 0.333...
    assert abs(main.dice_coefficient(a, b, 2) - 0.3333) < 0.01

def test_levenshtein():
    assert main.levenshtein('kitten', 'sitting') == 3
    assert main.levenshtein('abc', 'abc') == 0

def test_lcs_len():
    assert main.lcs_len('abcdef', 'abdf') == 4  # 'abdf'
    assert main.lcs_len('abc', 'abc') == 3

if __name__ == '__main__':
    test_normalize()
    test_ngrams()
    test_dice_coefficient()
    test_levenshtein()
    test_lcs_len()
    print("测试通过")
