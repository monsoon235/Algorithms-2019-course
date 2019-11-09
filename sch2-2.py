from typing import List
from copy import deepcopy

n: int
k: int
t: List[int]

now_arr: List[List[int]]  # 安排进的工作
finished_time: List[int]  # 每个机器的最后完成时间

best_arr: List[List[int]]  # 最佳安排
best_finished_time: int  # 最佳安排的结束时间


def get_arr(num: int):  # 分配工作 num
    global n, k, t, now_arr, finished_time, best_arr, best_finished_time
    if num >= n and max(finished_time) < best_finished_time:
        best_finished_time = max(finished_time)
        best_arr = deepcopy(now_arr)
        return
    if max(finished_time) >= best_finished_time:
        return
    for i in range(k):
        now_arr[i].append(num)
        finished_time[i] += t[num]
        get_arr(num + 1)
        now_arr[i].remove(num)
        finished_time[i] -= t[num]


if __name__ == '__main__':
    last_finished_time = 0
    n = 10
    k = 3
    t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    now_arr = [[] for _ in range(k)]
    finished_time = [0 for _ in range(k)]
    best_finished_time = sum(t) + 1
    get_arr(0)
    print(best_arr)
