def lcs_len(a, b, diff_threshold=0.5):
    la, lb = len(a), len(b)
    if max(la, lb) == 0:
        return 0
    if abs(la - lb) / max(la, lb) > diff_threshold:
        return 0  # 差异太大直接返回0
    dp = [[0]*(lb+1) for _ in range(la+1)]
    for i in range(la-1, -1, -1):
        for j in range(lb-1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i+1][j+1]
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j+1])
    return dp[0][0]
