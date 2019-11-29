from typing import List, Iterable
from copy import deepcopy
import time
import random
import math
import pandas as pd

task_num_global: int  # 任务数量
task_cost_global: List[float]  # 每个任务的 cost
machine_num_global: int  # 机器数量

now_arrangement: List[List[int]]  # 安排进的工作
finished_time: List[float]  # 每个机器的完成时间
best_arrangement: List[List[int]]  # 最佳安排
best_finished_time: float  # 最佳安排的结束时间


def get_best_arrangement_recursive(num: int):  # num 为当前要分配的任务编号
    global task_num_global, machine_num_global, task_cost_global, \
        now_arrangement, finished_time, \
        best_arrangement, best_finished_time
    max_time = max(finished_time)  # 所有工作都完成的时间
    # 找到更优安排
    if num >= task_num_global and max_time < best_finished_time:
        best_finished_time = max_time
        best_arrangement = deepcopy(now_arrangement)
        return
    # 剪枝
    if max_time >= best_finished_time:
        return
    # 把编号为 num+1 的任务依次尝试分配到每个机器中
    for i in range(machine_num_global):
        now_arrangement[i].append(num)
        finished_time[i] += task_cost_global[num]
        get_best_arrangement_recursive(num + 1)
        now_arrangement[i].pop()
        finished_time[i] -= task_cost_global[num]


def get_best_arrangement(task_cost: List[float], machine_num: int) -> List[List[int]]:
    assert machine_num > 0
    assert len(task_cost) > 0
    global task_num_global, machine_num_global, task_cost_global, \
        now_arrangement, finished_time, best_finished_time
    # 初始化全局变量
    task_num_global = len(task_cost)
    task_cost_global = task_cost
    machine_num_global = machine_num
    now_arrangement = [[] for _ in range(machine_num)]
    finished_time = [0 for _ in range(machine_num)]
    best_finished_time = math.inf
    # 递归回溯
    get_best_arrangement_recursive(0)
    return best_arrangement


# def test(task_num_range: Iterable[int], machine_num_range: Iterable[int]) -> None:
#     result = pd.DataFrame(
#         index=pd.Index(task_num_range, name='task_num'),
#         columns=pd.Index(machine_num_range, name='machine_num'),
#         dtype=float
#     )
#     for a in task_num_range:
#         for b in machine_num_range:
#             costs = [random.random() for _ in range(a)]
#             start = time.time()
#             get_best_arrangement(costs, b)
#             end = time.time()
#             result.loc[a, b] = end - start
#             print(a, b, (end - start) / (a ** b) * 1e5)
#     print('running time:')
#     print(result)
#     print()


if __name__ == '__main__':
    task_cost = [1, 7, 4, 10, 9, 4, 8, 8, 2, 4]
    machine_num = 5
    best_arrangement = get_best_arrangement(task_cost, machine_num)
    # 打印每个机器和安排在其上的任务
    print(
        '\n'.join(
            f'machine-{i}:\t' + ',\t'.join(
                f'task-{j}: {task_cost[j]}'
                for j in best_arrangement[i]
            )
            for i in range(machine_num)
        )
    )
    # print()
    # 测试时间复杂度
    # test(list(range(1, 10)), list(range(1, 10)))
