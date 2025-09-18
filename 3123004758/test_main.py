import unittest
import os
from normalize import normalize
from ngram import ngrams, dice_coefficient
from edit_distance import levenshtein
from lcs import lcs_len
from similarity import compute_similarity
from file_utils import read_file

class TestMain(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize('Hello, 世界! 123'), 'hello世界123')

    def test_ngrams(self):
        self.assertEqual(ngrams('abcd', 2), ['ab', 'bc', 'cd'])

    def test_dice_coefficient(self):
        a = 'abcd'
        b = 'abef'
        self.assertAlmostEqual(dice_coefficient(a, b, 2), 0.3333, places=2)

    def test_levenshtein(self):
        self.assertEqual(levenshtein('kitten', 'sitting'), 3)
        self.assertEqual(levenshtein('abc', 'abc'), 0)

    def test_lcs_len(self):
        self.assertEqual(lcs_len('abcdef', 'abdf'), 4)  # 'abdf'
        self.assertEqual(lcs_len('abc', 'abc'), 3)

    def test_compute_similarity(self):
        res = compute_similarity('abc', 'abc')
        self.assertAlmostEqual(res['score'], 1.0, places=6)
        res2 = compute_similarity('abc', 'xyz')
        self.assertLess(res2['score'], 0.1)

    def test_read_file(self):
        test_path = 'testfile.txt'
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write('hello world')
        self.assertEqual(read_file(test_path), 'hello world')
        os.remove(test_path)

if __name__ == '__main__':
    unittest.main()
