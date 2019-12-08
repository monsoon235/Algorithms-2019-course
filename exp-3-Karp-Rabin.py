import random
import string
import time
from functools import reduce

import numpy as np
import pandas as pd
from typing import List


# T 为待匹配串，P 为模式串
def match_Karp_Rabin(T: str, P: str) -> List[int]:
    n = len(T)
    m = len(P)
    if m > n:  # 模式串比待匹配串长，返回空
        return []
    rune_set = set(T + P)  # T 和 P 中所有 unicode 码点
    d = len(rune_set)  # 出现的 unicode 数量
    rune_to_int = dict(zip(rune_set, range(d)))  # 把 unicode 码点映射到 int
    q = 999983  # q 为 使得 dq 在 int32 表示范围内的一个较大质数
    h = pow(d, m - 1, q)  # h = d**(m-1) % q, 内置的 pow 函数可以更快速计算
    offset = []  # 匹配时 P 相对于 T 的偏移量
    # 初始化 p_hash t_hash
    p_hash = reduce(lambda hash, c: (d * hash + rune_to_int[c]) % q, P, 0)  # p 为 P 的 hash 值
    t_hash = reduce(lambda hash, c: (d * hash + rune_to_int[c]) % q, T[:m], 0)  # t 为 当前检测时 T 子串的 hash 值
    # shift 为 P 相对于 T 开始的偏移量
    for shift in range(n - m + 1):
        if p_hash == t_hash:
            # 检测伪命中
            if all(P[j] == T[j + shift] for j in range(m)):
                offset.append(shift)  # 不是伪命中，则加入到偏移量列表
        if shift < n - m:  # 更新 t_hasp
            # 此方法只需要 O(1) 的时间即可获得子串向右偏移一位时的新 hash
            # 而不用耗费 O(m) 的时间重新计算
            t_hash = (d * (t_hash - h * rune_to_int[T[shift]])
                      + rune_to_int[T[shift + m]]) % q
    return offset


def get_random_str(n: int) -> str:
    assert n > 0
    return ''.join(random.choice(string.ascii_letters + string.digits)
                   for _ in range(n))


# 穷举法
def get_std_answer(T: str, P: str) -> List[int]:
    n = len(T)
    m = len(P)
    ret = []
    for offset in range(n - m):
        if T[offset:m + offset] == P:
            ret.append(offset)
    return ret  # 返回所有在 T 中的匹配位置


if __name__ == '__main__':
    # 性能测试与正确性检验
    n_list = list(range(10 ** 5, 10 ** 6 + 1, 10 ** 5))
    m_list = list(range(10 ** 3, 5 * 10 ** 3 + 1, 10 ** 3))
    time_cost = pd.DataFrame(
        index=pd.Index(n_list, name='n'),
        columns=pd.Index(m_list, name='m'),
        dtype=float
    )
    for m in m_list:
        for n in n_list:
            T = get_random_str(n)
            P = get_random_str(m)
            start = time.time()
            offsets = match_Karp_Rabin(T, P)
            end = time.time()
            assert offsets == get_std_answer(T, P), f'error occurs when n={n}, m={m}'
            time_cost.loc[n, m] = end - start
            print(f'n={n}, m={m}, time={end - start} s')
    print(time_cost)
    mn_matrix = np.array([
        [m + n for m in m_list] for n in n_list
    ])
    print(time_cost * 10 ** 7 / mn_matrix)
