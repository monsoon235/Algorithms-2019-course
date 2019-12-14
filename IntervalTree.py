import random
import time
import math
import gc
from typing import Tuple
from enum import Enum, unique


@unique
class Color(Enum):
    Red = 0
    Black = 1


class Interval:
    @property
    def low(self):
        return self.__low

    @low.setter
    def low(self, value):
        if not isinstance(value, type(self.__low)):
            raise TypeError(f"'low must be instance of '{type(self.low)}'")
        self.__low = value

    @property
    def high(self):
        return self.__high

    @high.setter
    def high(self, value):
        if not isinstance(value, type(self.__high)):
            raise TypeError(f"'high must be instance of '{type(self.low)}'")
        self.__high = value

    def __init__(self, low, high) -> None:
        if not isinstance(low, type(high)):
            raise TypeError("'low' and 'high' must be same type")
        assert low is not None and high is not None
        self.__low = low
        self.__high = high

    def __str__(self) -> str:
        return f'[{self.low}, {self.high}]'


class Node:

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        if not isinstance(value, Color):
            raise TypeError("'color' must be instance of 'Color'")
        self.__color = value

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value):
        if not isinstance(value, Interval):
            raise TypeError("'interval' must be instance of 'Interval'")
        self.__interval = value

    @property
    def key(self):
        return self.interval.low

    @property
    def max(self):
        return self.__max

    @max.setter
    def max(self, value):
        if not isinstance(value, type(self.__max)):
            raise TypeError(f"'max' must be instance of '{type(self.__max)}'")
        self.__max = value

    @property
    def parent(self):
        assert self.__parent is not None
        return self.__parent

    @parent.setter
    def parent(self, value):
        if not isinstance(value, Node):
            raise TypeError("'parent' must be instance of 'Node'")
        self.__parent = value

    @property
    def left(self):
        assert self.__left is not None
        return self.__left

    @left.setter
    def left(self, value):
        if not isinstance(value, Node):
            raise TypeError("'left' must be instance of 'Node'")
        self.__left = value

    @property
    def right(self):
        assert self.__right is not None
        return self.__right

    @right.setter
    def right(self, value):
        if not isinstance(value, Node):
            raise TypeError("'right' must be instance of 'Node'")
        self.__right = value

    def __init__(self, color: Color, interval: Interval, parent=None, left=None, right=None) -> None:
        self.__color = color
        self.__interval = interval
        self.__max = interval.high
        if parent is not None:
            self.__parent = parent
        if left is not None:
            self.__left = left
        if right is not None:
            self.__right = right

    def __str__(self) -> str:
        if self.color == Color.Red:
            return f'\x1b[38;2;255;0;0m{self.interval}, max={self.max}\x1b[0m'
        else:
            return f'{self.interval}, max={self.max}'

    def fixMax(self):
        self.max = max(self.interval.high, self.left.max, self.right.max)


class RedBlackTree:
    nil: Node
    root: Node

    def __init__(self) -> None:
        self.clear()

    def clear(self):
        self.nil = Node(Color.Black, Interval(-math.inf, -math.inf))
        self.nil.parent = self.nil
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.root = self.nil

    def max_fixup(self, node: Node):
        now = node
        while now is not self.nil:
            now.fixMax()
            now = now.parent

    # 将 replacement 移植到 replaced 的位置
    def transplant(self, replaced: Node, replacement: Node):
        if replaced is self.root:
            self.root = replacement
        elif replaced is replaced.parent.left:
            replaced.parent.left = replacement
        else:
            replaced.parent.right = replacement
        replacement.parent = replaced.parent

    def left_rotate(self, node: Node):
        x = node
        y = x.right
        x.right = y.left
        if y.left is not self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x is self.root:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        # 修正 max
        x.fixMax()
        y.fixMax()

    def right_rotate(self, node: Node):
        y = node
        x = y.left
        y.left = x.right
        if x.right is not self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y is self.root:
            self.root = x
        elif y is y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x
        # 修正 max
        y.fixMax()
        x.fixMax()

    def insert(self, interval):
        z = Node(Color.Red, interval, self.nil, self.nil, self.nil)
        self.insert_node(z)

    # 修正 insert 之后的颜色问题
    def insert_fixup(self, node: Node):
        z = node
        # z 的颜色为 红，父节点不能是红
        while z.parent.color == Color.Red:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == Color.Red:  # case 1
                    z.parent.color = Color.Black
                    y.color = Color.Black
                    z.parent.parent.color = Color.Red
                    z = z.parent.parent
                else:
                    if z is z.parent.right:  # case 2
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = Color.Black  # case 3
                    z.parent.parent.color = Color.Red
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == Color.Red:  # case 4
                    z.parent.color = Color.Black
                    y.color = Color.Black
                    z.parent.parent.color = Color.Red
                    z = z.parent.parent
                else:
                    if z is z.parent.left:  # case 5
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = Color.Black  # case 6
                    z.parent.parent.color = Color.Red
                    self.left_rotate(z.parent.parent)
        self.root.color = Color.Black

    def insert_node(self, node: Node):
        node.left = self.nil
        node.right = self.nil
        node.color = Color.Red
        now = self.root  # 当前查找结点
        pre = now.parent  # 当前节点的父节点, 引入 pre 的作用在于 nil.parent 无定义
        while now is not self.nil:
            pre = now
            if node.key < now.key:
                now = now.left
            else:
                now = now.right
        # 查找到 node 的插入位置
        # 此时 now 一定是 nil
        assert now is self.nil
        node.parent = pre
        if now is self.root:
            self.root = node
        elif node.key < pre.key:
            pre.left = node
        else:
            pre.right = node

        # 区间树需要修正 max
        self.max_fixup(node)
        self.insert_fixup(node)

    def delete(self, interval):
        key = interval.low
        if self.root is self.nil:
            return
        now = self.root
        while now is not self.nil:
            if key == now.key:
                self.delete_node(now)
                return
            elif key < now.key:
                now = now.left
            else:
                now = now.right

    def delete_fixup(self, node: Node):
        x = node
        while x is not self.root and x.color == Color.Black:
            if x is x.parent.left:
                w = x.parent.right
                if w.color == Color.Red:
                    w.color = Color.Black
                    x.parent.color = Color.Red
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == Color.Black and w.right.color == Color.Black:
                    w.color = Color.Red
                    x = x.parent
                else:
                    if w.right.color == Color.Black:
                        w.left.color = Color.Black
                        w.color = Color.Red
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = Color.Black
                    w.right.color = Color.Black
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == Color.Red:
                    w.color = Color.Black
                    x.parent.color = Color.Red
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.left.color == Color.Black and w.right.color == Color.Black:
                    w.color = Color.Red
                    x = x.parent
                else:
                    if w.left.color == Color.Black:
                        w.right.color = Color.Black
                        w.color = Color.Red
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Color.Black
                    w.left.color = Color.Black
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = Color.Black

    def delete_node(self, node: Node):
        z = node
        if z.left is self.nil or z.right is self.nil:  # case 1, 2
            y = z  # y 是真正要删的点
        else:
            y = self.min_node(z.right)  # case 3
        if y.left is not self.nil:
            x = y.left
        else:
            x = y.right
        self.transplant(y, x)
        if y is not z:  # case 3
            z.interval = y.interval
        self.max_fixup(x.parent)
        if y.color == Color.Black:  # 删除黑节点需要 fixup
            self.delete_fixup(x)

    def find_by_index_recursive(self, now: Node, index: int) -> Tuple[Node, int]:
        if now is self.nil:
            return self.nil, index
        l, index = self.find_by_index_recursive(now.left, index)
        if l is not self.nil:
            return l, index
        if index == 0:
            return now, index
        index -= 1
        r, index = self.find_by_index_recursive(now.right, index)
        if r is not self.nil:
            return r, index
        return self.nil, index

    def delete_by_index(self, index: int):
        if index < 0:
            return
        node, _ = self.find_by_index_recursive(self.root, index)
        if node is not self.nil:
            self.delete_node(node)

    def min_node(self, sub_root: Node):
        if sub_root is self.nil:
            return self.nil
        now = sub_root
        while now.left is not self.nil:
            now = now.left
        return now

    # 如果正常则返回黑高，异常返回 -1
    def check_recursive(self, node: Node, pre_node: Node) -> int:
        if node is self.nil:
            return 0
        if node.color == Color.Red and (node.left.color == Color.Red or node.right.color == Color.Red):
            return -1
        l = self.check_recursive(node.left, pre_node)
        if pre_node is not self.nil and pre_node.key > node.key:
            return -1
        if node.left is not self.nil and node.left.parent is not node:
            return -1
        if node.right is not self.nil and node.right.parent is not node:
            return -1
        if node.max != max(node.interval.high, node.left.max, node.right.max):
            exit(-1)
            return -1
        r = self.check_recursive(node.right, node)
        if l == r and l != -1:
            if node.color == Color.Red:
                return l
            else:
                return l + 1
        else:
            return -1

    # 检查是否满足红黑树的性质
    def check(self) -> bool:
        if self.root.parent is not self.nil or self.root.color != Color.Black or self.nil.color != Color.Black:
            return False
        return self.check_recursive(self.root, self.nil) != -1

    def get_str_recursive(self, node: Node, depth: int) -> str:
        if node is self.nil:
            return ''
        l = self.get_str_recursive(node.left, depth + 1)
        r = self.get_str_recursive(node.right, depth + 1)
        prefix = '  ' * depth + '+~'
        return l + prefix + f'{node}\n' + r

    def __str__(self) -> str:
        return self.get_str_recursive(self.root, 0)


if __name__ == '__main__':
    tree = RedBlackTree()
    n = 0
    print('===== 正确性测试 =====')
    for _ in range(1000):
        if random.random() > 1 / 3 or n <= 0:
            low = random.randint(0, 999)
            key = Interval(low, low + random.randint(0, 999))
            print(f'\t> insert key = {key}')
            tree.insert(key)
            n += 1
            # print(tree)
        else:
            index = random.randint(0, n - 1)
            print(f'\t> delete index = {index}')
            tree.delete_by_index(index)
            n -= 1
            # print(tree)
        assert tree.check()
    print('===== 正确性测试通过 =====')
    print()
    print('===== 性能测试 =====')
    gc.disable()  # 避免 gc 造成性能波动
    tree.clear()
    last_n = 0
    for k in range(1, 21, 1):
        n = 2 ** k
        delta = n - last_n
        last_n = n
        for _ in range(delta):
            low = random.randint(0, 999)
            high = random.randint(low, 999 + 1)
            tree.insert(Interval(low, high))
        insert_sum_time = 0
        delete_sum_time = 0
        repeat_times = 10000
        for _ in range(repeat_times):
            low = random.randint(0, 999)
            high = random.randint(low, 999 + 1)
            interval = Interval(low, high)
            start = time.time()
            tree.insert(interval)
            end = time.time()
            insert_sum_time += end - start
            start = time.time()
            tree.delete(interval)
            end = time.time()
            delete_sum_time += end - start
        print(f'n=2^{k}\n\tinsert cost sum = {insert_sum_time} s\n\tdelete cost sum = {delete_sum_time} s')
    gc.enable()
    gc.collect()
    print('===== 性能测试结束 =====')
