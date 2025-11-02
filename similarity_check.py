# lcs_similarity.py

def lcs_length(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    return dp[m][n]

def lcs_similarity(a, b):
    return lcs_length(a, b) / min(len(a), len(b)) if min(len(a), len(b)) > 0 else 0

def average_lcs_similarity(comments):
    total = 0
    count = 0
    for i in range(len(comments)):
        for j in range(i+1, len(comments)):
            total += lcs_similarity(comments[i], comments[j])
            count += 1
    return round(total / count, 2) if count > 0 else 0