import gc
from typing import List, Optional, Any
import numpy as np
from enum import Enum, unique


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
    __pre: Optional[Any]
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

    def __str__(self) -> str:
        return str(self.id)


class Edge:
    pass


class CSR_Matrix:
    row_start_offset: List
    vertexes: List[Vertex]
    col_offset: List
    edges: List[Edge]

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
            self.row_start_offset = [None for _ in range(vertex_num)]
            self.vertexes = [Vertex(id) for id in sorted(v)]
            self.col_offset = [None for _ in range(edge_num)]
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

    def BFS(self, start: Vertex, action):
        for v in self.vertexes:
            v.color = Color.WHITE
            v.depth = len(self.edges) + 1
            v.pre = None
        s = start
        s.color = Color.GRAY
        s.depth = 0
        s.pre = None
        action(s)
        Q = [s]
        while len(Q) != 0:
            s = Q.pop(0)
            for v in self.get_adj_vertexes(s):
                if v.color == Color.WHITE:
                    v.color = Color.GRAY
                    v.depth = s.depth + 1
                    v.pre = s
                    action(v)
                    Q.append(v)
            s.color = Color.BLACK

    def bidirectional_BFS(self, start: Vertex, end: Vertex) -> List[Vertex]:
        if start is end:
            return [start]
        for v in self.vertexes:
            v.color = Color.WHITE
            v.depth = len(self.edges) + 1
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
        while len(P) != 0 and len(Q) != 0:
            s = P.pop(0)
            for v in self.get_adj_vertexes(s):
                if v.color == Color.GRAY2:  # 从另一边访问过的顶
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
            t = Q.pop(0)
            for v in self.get_adj_vertexes(t):
                if v.color == Color.GRAY1:
                    bridge1 = v
                    bridge2 = t
                    success = True
                elif v.color == Color.WHITE:
                    v.color = Color.GRAY2
                    v.depth = t.depth + 1
                    v.pre = t
                    Q.append(v)
            t.color = Color.BLACK2
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
            return list(reversed(chain1)) + chain2
        else:
            return []


if __name__ == '__main__':
    matrix = CSR_Matrix()
    matrix.load_from_file('facebook_combined.txt')
    matrix.BFS(matrix.vertexes[0], action=lambda v: print(f'visit {v}'))
    print([v.id for v in
           matrix.bidirectional_BFS(matrix.vertexes[0], matrix.vertexes[2333])
           ])
    for v in matrix.vertexes:
        chain = matrix.bidirectional_BFS(matrix.vertexes[0], v)
        print([v.id for v in chain])
        if not chain:
            print(f'{0} and {v} are not connected')
