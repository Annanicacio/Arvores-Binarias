# rbt.py
from metrics import Metrics

class RBTNode:
    def __init__(self, id, name, extra=None, color=1):
        self.id = id
        self.name = name
        self.extra = extra
        self.color = color # 1 = RED, 0 = BLACK
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = RBTNode(0, "", None, color=0) # Sentinela PRETO
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
        self.metrics = Metrics()

    # ----------------- Inserção -----------------
    def insert(self, id, name, extra=None):
        node = RBTNode(id, name, extra, color=1)
        node.left = self.TNULL
        node.right = self.TNULL
        self.metrics.nodes += 1
        
        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            self.metrics.comparisons += 1
            if node.id < x.id:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.id < y.id:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = 0 
            return

        if node.parent.parent is None:
            return

        self._fix_insert(node)

    def _fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self._left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self._right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    # ----------------- Remoção -----------------
    def delete(self, id):
        node = self.search(id)
        if node != self.TNULL and node is not None:
            self._delete_node(node)
            self.metrics.nodes -= 1

    def _delete_node(self, z):
        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self._rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self._rb_transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 0:
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self._left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self._right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self._right_rotate(x.parent)
                    s = x.parent.left
                if s.right.color == 0 and s.left.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self._left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def _rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # ----------------- Rotações -----------------
    def _left_rotate(self, x):
        self.metrics.rotations += 1
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        self.metrics.rotations += 1
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # ----------------- Auxiliares -----------------
    def search(self, id):
        return self._search_helper(self.root, id)

    def _search_helper(self, node, id):
        if node == self.TNULL or id == node.id:
            return node if node != self.TNULL else None
        
        self.metrics.comparisons += 1
        if id < node.id:
            return self._search_helper(node.left, id)
        return self._search_helper(node.right, id)

    def _minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def height(self):
        def _h(node):
            if node == self.TNULL: return 0
            return 1 + max(_h(node.left), _h(node.right))
        return _h(self.root)

    def count_nodes(self):
        return self.metrics.nodes

    def reset_metrics(self):
        self.metrics.reset()