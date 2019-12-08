import string
import time
import numpy as np
import pandas as pd
from enum import Enum, unique
from typing import List
import random


@unique
class Direction(Enum):
    Left: str = '←'
    Up: str = '↑'
    Left_Up: str = '↖'


# 获取 LCS
def get_LCS(b: np.ndarray, s1: str, i: int, j: int, output: List[str]):
    if i == 0 or j == 0:
        return
    # s1 和 s2 的最后一个字符相等的情况，则这个字符加入到 LCS
    if b[i, j] == Direction.Left_Up:
        get_LCS(b, s1, i - 1, j - 1, output)
        output.append(s1[i - 1])
    # 其他两种情况，分别去掉 s1 中的最后一个字符或 s2 中的最后一个字符，进行递归
    elif b[i, j] == Direction.Up:
        get_LCS(b, s1, i - 1, j, output)
    else:
        get_LCS(b, s1, i, j - 1, output)


def longest_common_subsequence(s1: str, s2: str) -> str:
    m: int = len(s1)  # s1 长度
    n: int = len(s2)  # s2 长度
    # 初始化 b c 矩阵
    b = np.empty(shape=(len(s1) + 1, len(s2) + 1), dtype=Direction)
    c = np.empty(shape=(len(s1) + 1, len(s2) + 1), dtype=int)
    # c 的递推边界设为 0
    c[:, 0] = 0
    c[0, :] = 0
    # 计算 c[i, j]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # s1 和 s2 的最后一个字符相等，这个字符可能是 LCS 的字符
            if s1[i - 1] == s2[j - 1]:
                c[i, j] = c[i - 1, j - 1] + 1
                b[i, j] = Direction.Left_Up
                # b[i, j] = '↖'
            # 最后一个字符不相等，取 c[i-1,j] 和 c[i,j-1] 中较大的那个
            elif c[i - 1, j] >= c[i, j - 1]:
                c[i, j] = c[i - 1, j]
                b[i, j] = Direction.Up
                # b[i, j] = '↑'
            else:
                c[i, j] = c[i, j - 1]
                b[i, j] = Direction.Left
                # b[i, j] = '←'
    seq = []
    get_LCS(b, s1, m, n, seq)  # 用矩阵 b 获取 LCS
    return ''.join(seq)


def get_random_str(n: int) -> str:
    assert n > 0
    return ''.join(random.choice(string.ascii_letters + string.digits)
                   for _ in range(n))


if __name__ == '__main__':
    # 正确性测试
    s1 = '10010101'
    s2 = '010110110'
    seq = longest_common_subsequence(s1, s2)
    print(seq)

    # 性能测试
    m_list = list(range(200, 1501, 200))
    n_list = list(range(200, 1501, 200))
    time_cost = pd.DataFrame(
        index=pd.Index(m_list, name='m'),
        columns=pd.Index(n_list, name='n'),
        dtype=float
    )
    for m in m_list:
        for n in n_list:
            s1 = get_random_str(m)
            s2 = get_random_str(n)
            start = time.time()
            sub = longest_common_subsequence(s1, s2)
            end = time.time()
            time_cost.loc[m, n] = end - start
            print(f'm={m}, n={n}, time={end - start} s')
    print(time_cost)
    mn_matrix = np.array([
        [m * n for n in n_list] for m in m_list
    ])
    print(time_cost * 10 ** 6 / mn_matrix)
