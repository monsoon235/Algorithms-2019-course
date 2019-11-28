from typing import Tuple, List
from itertools import combinations
import math
import random
import time


# 计算距离
def get_dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# 递归分治寻找最近点
def min_dist_point_in_plane_recursive(X: List[Tuple[float, float]], Y: List[Tuple[float, float]]):
    assert len(X) == len(Y)
    n = len(X)  # 点的数量
    if n < 2:  # 点的数量小于 2, 返回 inf
        return None, None, math.inf
    if n <= 3:  # 点的数量是 2 或 3, 用穷举法，递归边界
        min_a, min_b = min(
            combinations(X, 2),  # 生成两个点的所有组合序列
            key=lambda pair: get_dist(pair[0], pair[1])
        )
        min_dist = get_dist(min_a, min_b)
        assert min_dist != math.inf
        return min_a, min_b, min_dist
    mid = X[n // 2][0]  # 点横坐标的中位数
    # 按中位数进行左右划分，仍保证左右 X, Y 有序
    XL = [p for p in X if p[0] <= mid]
    XR = [p for p in X if p[0] > mid]
    # todo 可能导致无限递归
    YL = [p for p in Y if p[0] <= mid]
    YR = [p for p in Y if p[0] > mid]
    # 递归寻找左右两边的最近点
    aL, bL, dist_L = min_dist_point_in_plane_recursive(XL, YL)
    aR, bR, dist_R = min_dist_point_in_plane_recursive(XR, YR)
    # 寻找左右最近点对中较小的一个
    if dist_L < dist_R:
        min_a, min_b, min_dist = aL, bL, dist_L
    else:
        min_a, min_b, min_dist = aR, bR, dist_R
    # 找到横坐标距 mid 小于等于 min_dist 点
    Y_apo = [p for p in Y if abs(p[0] - mid) <= 2 * min_dist]
    for i, a in enumerate(Y_apo):
        for b in Y_apo[i + 1:i + 8]:  # 每个点只需检查其后的 7 个点
            dist = get_dist(a, b)
            if dist < min_dist:
                min_a, min_b, min_dist = a, b, dist
    return min_a, min_b, min_dist  # 返回最近的两个点和之间的距离


# 分治法入口函数
def min_dist_point_in_plane(P: List[Tuple[float, float]]):
    # 分别按横纵坐标排序
    X = sorted(P, key=lambda x: x[0])
    Y = sorted(P, key=lambda x: x[1])
    return min_dist_point_in_plane_recursive(X, Y)


# 穷举法寻找解，用于比较时间和验证算法正确性
def min_dist_point_in_plane_by_simple_search(P: List[Tuple[float, float]]):
    min_a, min_b = min(
        combinations(P, 2),
        key=lambda pair: get_dist(pair[0], pair[1])
    )
    return min_a, min_b, get_dist(min_a, min_b)


def test(P: List[Tuple[float, float]]):
    print(f'{len(P)} points:')
    # 分治法
    start = time.time()
    min_a, min_b, min_dist = min_dist_point_in_plane(P)
    time_by_recursion = time.time() - start
    print(f'\ttime usage by recursion: {time_by_recursion} s')
    # 穷举法
    start = time.time()
    std_a, std_b, std_dist = min_dist_point_in_plane_by_simple_search(P)
    time_by_search = time.time() - start
    print(f'\ttime usage by search: {time_by_search} s')
    # 检验算法正确性
    assert min_dist == std_dist, 'test failed'
    assert (min_a == std_a and min_b == std_b) \
           or (min_a == std_b and min_b == std_a), 'test failed'
    print('test success')
    print(f'\ta: {min_a}')
    print(f'\tb: {min_b}')
    print(f'\tdist: {min_dist}')
    print()


if __name__ == '__main__':
    # 测试点集
    P = [(12, 36), (5, 29), (25, 46), (32, 24),
         (54, 62), (48, 68), (30, 100), (52, 77),
         (26, 96), (61, 2), (10, 11), (8, 2)]
    test(P)
    # 随机点集
    for n in range(1000, 10001, 1000):
        P = [((random.random() - 0.5) * 10000,
              (random.random() - 0.5) * 10000)
             for _ in range(n)]
        test(P)
