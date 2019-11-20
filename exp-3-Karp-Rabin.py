import random
import string
from typing import List


def match_Karp_Rabin(T: str, P: str) -> List[int]:
    n = len(T)
    m = len(P)
    assert n >= m > 0
    rune_set = set(T + P)  # 所有 unicode 码点
    d = len(rune_set)
    rune_to_int = dict(zip(rune_set, range(d)))  # unicode 码点映射到 int
    q = 999983  # 获取使得 dq 在 int32 表示范围内的较大整数
    h = pow(d, m - 1, q)  # d**(m-1) % q
    p = 0
    t = 0
    ret = []  # 匹配时 P 的偏移量
    for i in range(m):
        p = (d * p + rune_to_int[P[i]]) % q  # 计算代表 p 的数
        t = (d * t + rune_to_int[T[i]]) % q  # 初始化 t
    for shift in range(n - m + 1):  # shift 为当前偏移量
        if p == t:
            if all(P[j] == T[j + shift] for j in range(m)):  # 检测伪命中
                print(f'Pattern occurs with shift {shift}')
                ret.append(shift)
        if shift < n - m:  # 更新 t
            t = (d * (t - h * rune_to_int[T[shift]])
                 + rune_to_int[T[shift + m]]) % q
    return ret


def get_random_str(n: int) -> str:
    assert n > 0
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


if __name__ == '__main__':
    T = get_random_str(2 ** 8)
    P = get_random_str(8)
    print(match_Karp_Rabin(T, P))
    T = get_random_str(2 ** 11)
    P = get_random_str(16)
    print(match_Karp_Rabin(T, P))
    T = get_random_str(2 ** 14)
    P = get_random_str(32)
    print(match_Karp_Rabin(T, P))
    print(match_Karp_Rabin('333333333333333', '333'))
