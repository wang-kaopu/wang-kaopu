import unittest
import main
import os

class TestMain(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(main.normalize('Hello, 世界! 123'), 'hello世界123')

    def test_ngrams(self):
        self.assertEqual(main.ngrams('abcd', 2), ['ab', 'bc', 'cd'])

    def test_dice_coefficient(self):
        a = 'abcd'
        b = 'abef'
        # 2-gram: ab, bc, cd vs ab, be, ef
        # 交集: ab
        # 总数: 3+3=6
        # dice = 2*1/6 = 0.333...
        self.assertAlmostEqual(main.dice_coefficient(a, b, 2), 0.3333, places=2)

    def test_levenshtein(self):
        self.assertEqual(main.levenshtein('kitten', 'sitting'), 3)
        self.assertEqual(main.levenshtein('abc', 'abc'), 0)

    def test_lcs_len(self):
        self.assertEqual(main.lcs_len('abcdef', 'abdf'), 4)  # 'abdf'
        self.assertEqual(main.lcs_len('abc', 'abc'), 3)

    def test_compute_similarity(self):
        res = main.compute_similarity('abc', 'abc')
        self.assertAlmostEqual(res['score'], 1.0, places=6)
        res2 = main.compute_similarity('abc', 'xyz')
        self.assertLess(res2['score'], 0.1)

    def test_read_file(self):
        test_path = 'testfile.txt'
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write('hello world')
        self.assertEqual(main.read_file(test_path), 'hello world')
        os.remove(test_path)

if __name__ == '__main__':
    unittest.main()
