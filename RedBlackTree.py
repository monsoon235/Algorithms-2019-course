import enum


class RedBlackTreeNode:
    def __init__(self, color: str, key, left=None, right=None, parent=None) -> None:
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent
        self.key = key

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, new_color: str):
        if not isinstance(new_color, str):
            raise TypeError("'color' must be 'r', 'red', 'b' or 'black'")
        if new_color in ('r', 'red'):
            self.__color = 'red'
        elif new_color in ('b', 'black'):
            self.__color = 'black'
        else:
            raise ValueError("'color' must be 'r', 'red', 'b' or 'black'")

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, new_left):
        if new_left is not None and not isinstance(new_left, RedBlackTreeNode):
            raise TypeError("'left' must be RedBlackTreeNode")
        self.__left = new_left

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, new_right):
        if new_right is not None and not isinstance(new_right, RedBlackTreeNode):
            raise TypeError("'right' must be RedBlackTreeNode")
        self.__right = new_right

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, new_parent):
        if new_parent is not None and not isinstance(new_parent, RedBlackTreeNode):
            raise TypeError("'parent' must be RedBlackTreeNode")
        self.__parent = new_parent

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, new_key):
        self.__key = new_key


class RedBlackTree:

    def __init__(self, root_key=None) -> None:
        if root_key is None:
            self.__root=None
        self.__root = RedBlackTreeNode('b', root_key)

    @property
    def root(self):
        return self.__root

    def insert(self, key):
        now = self.root
        while now is not None:
            if key < now.key:
                now = now.left
            else:
                now = now.right
        node = RedBlackTreeNode(color='red', key=key, parent=now.parent)
        if


if __name__ == '__main__':
    RedBlackTree('233')
