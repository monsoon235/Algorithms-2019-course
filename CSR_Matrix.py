import gc
from typing import List
import numpy as np
from enum import Enum, unique
import time
import random


@unique
class Color(Enum):
    WHITE = 0
    GRAY = 1
    BLACK = 2
    BLACK1 = 3
    BLACK2 = 4
    GRAY1 = 5
    GRAY2 = 6


class Vertex:
    __color: Color
    __depth: int

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        assert isinstance(value, Color)
        self.__color = value

    @property
    def depth(self):
        return self.__depth

    @depth.setter
    def depth(self, value):
        assert isinstance(value, int)
        assert value >= 0
        self.__depth = value

    @property
    def pre(self):
        return self.__pre

    @pre.setter
    def pre(self, value):
        assert isinstance(value, Vertex) or value is None
        self.__pre = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    def __init__(self, id) -> None:
        self.id = id
        self.pre = None
        self.depth = 0
        self.color = Color.WHITE

    def __str__(self) -> str:
        return str(self.id)


class Edge:
    pass


class CSR_Matrix:
    row_start_offset: List[int]
    vertexes: List[Vertex]  # 每个顶的信息
    col_offset: List[int]
    edges: List[Edge]  # 每个边的信息

    def __init__(self) -> None:
        self.row_start_offset = []
        self.vertexes = []
        self.col_offset = []
        self.edges = []

    def load_from_file(self, path_to_file: str):
        # 数据集已经预排序
        with open(path_to_file, 'r') as f:
            pairs = f.readlines()
            # 找出所有点
            v = set()
            for pair in pairs:
                a, b = map(int, pair.split(sep=' '))
                v.add(a)
                v.add(b)
            vertex_num = len(v)
            edge_num = len(pairs) * 2
            # 先表示成邻接矩阵
            adj_matrix = np.zeros(shape=(vertex_num, vertex_num), dtype=bool)
            for pair in pairs:
                a, b = map(int, pair.split(sep=' '))
                adj_matrix[a, b] = True
                adj_matrix[b, a] = True
            # 再压缩成 CSR 格式
            self.row_start_offset = [-1 for _ in range(vertex_num)]
            self.vertexes = [Vertex(id) for id in sorted(v)]
            self.col_offset = [-1 for _ in range(edge_num)]
            self.edges = [Edge() for _ in range(edge_num)]
            edge_index = 0
            for i in range(adj_matrix.shape[0]):
                self.row_start_offset[i] = edge_index
                for j in range(adj_matrix.shape[1]):
                    if adj_matrix[i, j]:
                        self.col_offset[edge_index] = j
                        edge_index += 1
            assert edge_index == edge_num
        gc.collect()

    # 获得邻点
    def get_adj_vertexes(self, v: Vertex) -> List:
        if v.id == len(self.row_start_offset) - 1:
            return [
                self.vertexes[id]
                for id in self.col_offset[self.row_start_offset[v.id]:]
            ]
        else:
            return [
                self.vertexes[id]
                for id in self.col_offset[self.row_start_offset[v.id]:self.row_start_offset[v.id + 1]]
            ]

    def BFS(self, start: Vertex, end: Vertex) -> List[Vertex]:
        if start is end:  # 开始与结束重合的特殊情况
            return [start]
        for v in self.vertexes:
            v.color = Color.WHITE  # 标注为未访问
            v.pre = None
        s = start
        s.color = Color.GRAY
        s.depth = 0
        s.pre = None
        P = [s]  # P 为下次迭代要访问的顶
        success = False
        while len(P) != 0:
            s = P.pop(0)
            for v in self.get_adj_vertexes(s):
                if v is end:  # 成功找到 end
                    v.pre = s
                    success = True
                    break
                elif v.color == Color.WHITE:  # 未访问的顶标记为即将访问
                    v.color = Color.GRAY
                    v.depth = s.depth + 1  # 记录深度
                    v.pre = s  # 记录前驱
                    P.append(v)
            s.color = Color.BLACK  # 标记为访问过
            if success:
                break
        if success:
            chain = []
            s = end
            while s is not None:
                chain.append(s)
                s = s.pre
            chain.reverse()
            return chain
        else:
            return []

    def BFS_bidirectional(self, start: Vertex, end: Vertex) -> List[Vertex]:
        if start is end:
            return [start]
        for v in self.vertexes:
            v.color = Color.WHITE
            v.pre = None
        s = start
        s.color = Color.GRAY1
        s.depth = 0
        s.pre = None
        P = [s]
        t = end
        t.color = Color.GRAY2
        t.depth = 0
        t.pre = None
        Q = [t]
        bridge1 = None  # 两侧搜索的连通顶
        bridge2 = None
        success = False
        while len(P) != 0 or len(Q) != 0:
            # 先进行一侧的搜索
            for _ in range(len(P)):
                s = P.pop(0)
                for v in self.get_adj_vertexes(s):
                    # assert v.color != Color.BLACK2
                    if v.color == Color.GRAY2:  # v 为另一侧即将访问的点
                        bridge1 = s
                        bridge2 = v
                        success = True
                        break
                    elif v.color == Color.WHITE:
                        v.color = Color.GRAY1
                        v.depth = s.depth + 1
                        v.pre = s
                        P.append(v)
                s.color = Color.BLACK1
                if success:
                    break
            if success:
                break
            # 再进行另一侧的搜索
            for _ in range(len(Q)):
                t = Q.pop(0)
                for v in self.get_adj_vertexes(t):
                    # assert v.color != Color.BLACK1
                    if v.color == Color.GRAY1:
                        bridge1 = v
                        bridge2 = t
                        success = True
                        break
                    elif v.color == Color.WHITE:
                        v.color = Color.GRAY2
                        v.depth = t.depth + 1
                        v.pre = t
                        Q.append(v)
                t.color = Color.BLACK2
                if success:
                    break
            if success:
                break
        if success:
            chain1 = []
            while bridge1 is not None:
                chain1.append(bridge1)
                bridge1 = bridge1.pre
            chain2 = []
            while bridge2 is not None:
                chain2.append(bridge2)
                bridge2 = bridge2.pre
            assert chain1[len(chain1) - 1] is start
            assert chain2[len(chain2) - 1] is end
            chain1.reverse()
            return chain1 + chain2
        else:
            return []


def get_id_list(l: List[Vertex]) -> List[int]:
    return [v.id for v in l]


if __name__ == '__main__':
    matrix = CSR_Matrix()
    matrix.load_from_file('dataset/facebook_combined.txt')
    # 正确性测试与性能测试
    sum1 = 0
    sum2 = 0
    n = 2000
    for _ in range(n):
        v1 = matrix.vertexes[random.randint(0, len(matrix.vertexes) - 1)]
        v2 = matrix.vertexes[random.randint(0, len(matrix.vertexes) - 1)]
        start = time.time()
        path1 = matrix.BFS(v1, v2)
        sum1 += time.time() - start
        start = time.time()
        path2 = matrix.BFS_bidirectional(v1, v2)
        sum2 += time.time() - start
        if len(path1) != len(path2):
            print(f'error occurs!')
            print(f'path by BFS = {get_id_list(path1)}')
            print(f'path by bidirectional BFS = {get_id_list(path2)}')
            print()
    print(f'avg time for BFS = {sum1 / n}')
    print(f'avg time for bidirectional BFS = {sum2 / n}')
