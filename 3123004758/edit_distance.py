try:
    import Levenshtein
    def levenshtein(a, b):
        return Levenshtein.distance(a, b)
except ImportError:
    def levenshtein(a, b):
        if a == b:
            return 0
        la, lb = len(a), len(b)
        if la == 0:
            return lb
        if lb == 0:
            return la
        prev = list(range(lb + 1))
        for i, ca in enumerate(a, 1):
            cur = [i] + [0] * lb
            for j, cb in enumerate(b, 1):
                cost = 0 if ca == cb else 1
                cur[j] = min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + cost)
            prev = cur
        return prev[lb]
