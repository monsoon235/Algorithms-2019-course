from typing import List
from copy import deepcopy

task_num: int
machine_num: int
task_cost: List[int]

now_arr: List[List[int]]  # 安排进的工作
finished_time: List[int]  # 每个机器的最后完成时间

best_arr: List[List[int]]  # 最佳安排
best_finished_time: int  # 最佳安排的结束时间


def get_arr(num: int):  # 分配工作 num
    global task_num, machine_num, task_cost, now_arr, finished_time, best_arr, best_finished_time
    max_time = max(finished_time)  # 最后停止工作的机器
    if num >= task_num and max_time < best_finished_time:  # 找到更优安排
        best_finished_time = max_time
        best_arr = deepcopy(now_arr)
        return
    if max_time >= best_finished_time:  # 剪枝
        return
    for i in range(machine_num):
        now_arr[i].append(num)
        finished_time[i] += task_cost[num]
        get_arr(num + 1)
        now_arr[i].pop()
        finished_time[i] -= task_cost[num]


if __name__ == '__main__':
    last_finished_time = 0
    task_num = 10
    machine_num = 5
    task_cost = [1, 7, 4, 10, 9, 4, 8, 8, 2, 4]
    now_arr = [[] for _ in range(machine_num)]
    finished_time = [0 for _ in range(machine_num)]
    best_finished_time = sum(task_cost) + 1
    get_arr(0)
    print(best_arr)
    print([[task_cost[i] for i in machine] for machine in best_arr])
