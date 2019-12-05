import random
from typing import Tuple
from enum import Enum, unique


@unique
class Color(Enum):
    Red = 0
    Black = 1


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
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = value

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

    def __init__(self, color: Color, key, parent=None, left=None, right=None) -> None:
        self.color = color
        self.key = key
        if parent is not None:
            self.parent = parent
        if left is not None:
            self.left = left
        if right is not None:
            self.right = right

    def __str__(self) -> str:
        if self.color == Color.Red:
            return f'\x1b[38;2;255;0;0m{self.key}\x1b[0m'
        else:
            return f'{self.key}'


class RedBlackTree:
    nil: Node
    root: Node

    def __init__(self) -> None:
        self.nil = Node(Color.Black, 'nil')
        self.nil.parent = self.nil
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.root = self.nil

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

    def insert(self, key):
        z = Node(Color.Red, key, self.nil, self.nil, self.nil)
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
        self.insert_fixup(node)

    def delete(self, key):
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
            z.key = y.key
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
        if random.random() > 1 / 2 or n <= 0:
            e = random.randint(0, 999)
            print(f'=== insert {e} ===')
            tree.insert(e)
            n += 1
            # print(tree)
        else:
            e = random.randint(0, n - 1)
            print(f'=== delete {e + 1}th ===')
            tree.delete_by_index(e)
            n -= 1
            # print(tree)
        assert tree.check()
    print('===== 正确性测试通过 =====')
    print()
    print('===== 性能测试 =====')

