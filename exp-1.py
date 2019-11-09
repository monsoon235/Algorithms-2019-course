from typing import Tuple, List, Iterable
from itertools import combinations
import math
import random


def recurse(X: List[Tuple[float, float]], Y: List[Tuple[float, float]]):
    assert len(X) == len(Y)
    n = len(X)
    if n < 2:
        return None, None, math.inf
    if n <= 3:
        min_a, min_b = min(
            combinations(X, 2),
            key=lambda pair: (pair[0][0] - pair[1][0]) ** 2 + (pair[0][1] - pair[1][1]) ** 2
        )
        min_dist = math.sqrt((min_a[0] - min_b[0]) ** 2 + (min_a[1] - min_b[1]) ** 2)
        assert min_dist != math.inf
        return min_a, min_b, min_dist
    mid = X[n // 2][0]
    XL = [p for p in X if p[0] <= mid]
    XR = [p for p in X if p[0] > mid]
    YL = [p for p in Y if p[0] <= mid]
    YR = [p for p in Y if p[0] > mid]
    aL, bL, dist_L = recurse(XL, YL)
    aR, bR, dist_R = recurse(XR, YR)
    if dist_L < dist_R:
        min_a = aL
        min_b = bL
        min_dist = dist_L
    else:
        min_a = aR
        min_b = bR
        min_dist = dist_R
    Y_apo = [p for p in Y if abs(p[0] - mid) <= 2 * min_dist]
    for i, a in enumerate(Y_apo):
        for b in Y_apo[i + 1:i + 8]:
            dist = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
            if dist < min_dist:
                min_a = a
                min_b = b
                min_dist = dist
    return min_a, min_b, min_dist


def min_dist_point_in_plane(P: Iterable[Tuple[float, float]]):
    X = sorted(P, key=lambda x: x[0])
    Y = sorted(P, key=lambda x: x[1])
    return recurse(X, Y)


if __name__ == '__main__':
    # P = [(random.random() * random.randint(0, 10000),
    #       random.random() * random.randint(0, 10000))
    #      for _ in range(10000)]
    P = [
        (12, 36),
        (5, 29),
        (25, 46),
        (32, 24),
        (54, 62),
        (48, 68),
        (30, 100),
        (52, 77),
        (26, 96),
        (61, 2),
        (10, 11),
        (8, 2),
    ]
    min_a, min_b, min_dist = min_dist_point_in_plane(P)
    print(min_a)
    print(min_b)
    print(min_dist)
