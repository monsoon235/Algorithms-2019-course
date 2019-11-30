import string
import numpy as np
from enum import Enum, unique
from typing import List
import random


@unique
class Direction(Enum):
    Left: str = '←'
    Up: str = '↑'
    Left_Up: str = '↖'


def get_LCS(b: np.ndarray, s1: str, i: int, j: int, output: List[str]):
    if i == 0 or j == 0:
        return
    if b[i, j] == Direction.Left_Up:
        get_LCS(b, s1, i - 1, j - 1, output)
        output.append(s1[i-1])
    elif b[i, j] == Direction.Up:
        get_LCS(b, s1, i - 1, j, output)
    else:
        get_LCS(b, s1, i, j - 1, output)


def longest_common_subsequence(s1: str, s2: str) -> str:
    m: int = len(s1)
    n: int = len(s2)
    b = np.empty(shape=(len(s1) + 1, len(s2) + 1), dtype=Direction)
    c = np.empty(shape=(len(s1) + 1, len(s2) + 1), dtype=int)
    c[:, 0] = 0
    c[0, :] = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                c[i, j] = c[i - 1, j - 1] + 1
                b[i, j] = Direction.Left_Up
                # b[i, j] = '↖'
            elif c[i - 1, j] >= c[i, j - 1]:
                c[i, j] = c[i - 1, j]
                b[i, j] = Direction.Up
                # b[i, j] = '↑'
            else:
                c[i, j] = c[i, j - 1]
                b[i, j] = Direction.Left
                # b[i, j] = '←'
    seq = []
    get_LCS(b, s1, m, n, seq)
    return ''.join(seq)


if __name__ == '__main__':
    # s1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(2 ** 8))
    # s2 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(2 ** 6))
    s1 = '10010101'
    s2 = '010110110'
    seq = longest_common_subsequence(s1, s2)
    print(seq)
