from typing import List

task_num: int
c: List[List[int]]

now_cost: int
now_arrangement: List[int]

min_cost: int
best_arrangement: List[int]


def work_arrange_recursive(arranged_num: int) -> None:
    global task_num, c, now_cost, now_arrangement, min_cost, best_arrangement
    if arranged_num >= n and now_cost < min_cost:  # 递归边界
        min_cost = now_cost
        best_arrangement = now_arrangement.copy()
        return
    if now_cost >= min_cost:  # 剪枝
        return
    for i in range(n):  # 遍历未分配工作，尝试分配
        if now_arrangement[i] == -1:  # 工作未被分配
            now_arrangement[i] = arranged_num  # 工作 i 分配给第 arranged_num 个人
            now_cost += c[i][arranged_num]
            work_arrange_recursive(arranged_num + 1)
            now_arrangement[i] = -1
            now_cost -= c[i][arranged_num]


if __name__ == '__main__':
    task_num = 2
    c = [
        [1, 2],
        [2, 10],
    ]
    now_cost = 0
    now_arrangement = [-1 for _ in range(task_num)]
    min_cost = sum(sum(row) for row in c) + 1
    work_arrange_recursive(0)
    print(best_arrangement)
