# avl.py
from metrics import Metrics

class AVLNode:
    def __init__(self, id, name, extra=None):
        self.id = id
        self.name = name
        self.extra = extra
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None
        self.metrics = Metrics()

    # ----------------- Inserção -----------------
    def insert(self, id, name, extra=None):
        self.root = self._insert(self.root, id, name, extra)

    def _insert(self, node, id, name, extra):
        if not node:
            self.metrics.nodes += 1
            return AVLNode(id, name, extra)
        
        self.metrics.comparisons += 1
        if id < node.id:
            node.left = self._insert(node.left, id, name, extra)
        else:
            node.right = self._insert(node.right, id, name, extra)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Rotações
        if balance > 1:
            self.metrics.comparisons += 1
            if id < node.left.id:
                self.metrics.rotations += 1
                return self._right_rotate(node)
            else:
                node.left = self._left_rotate(node.left)
                self.metrics.rotations += 2
                return self._right_rotate(node)
        
        if balance < -1:
            self.metrics.comparisons += 1
            if id > node.right.id:
                self.metrics.rotations += 1
                return self._left_rotate(node)
            else:
                node.right = self._right_rotate(node.right)
                self.metrics.rotations += 2
                return self._left_rotate(node)

        return node

    # ----------------- Remoção -----------------
    def delete(self, id):
        self.root = self._delete(self.root, id)

    def _delete(self, node, id):
        if not node:
            return node
        
        self.metrics.comparisons += 1
        if id < node.id:
            node.left = self._delete(node.left, id)
        elif id > node.id:
            node.right = self._delete(node.right, id)
        else:
            if not node.left or not node.right:
                temp = node.left if node.left else node.right
                if not temp:
                    temp = None
                    node = None
                else:
                    node = temp
                self.metrics.nodes -= 1
            else:
                temp = self._min(node.right)
                node.id, node.name, node.extra = temp.id, temp.name, temp.extra
                node.right = self._delete(node.right, temp.id)

        if node is None:
            return node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1:
            if self._get_balance(node.left) >= 0:
                self.metrics.rotations += 1
                return self._right_rotate(node)
            else:
                node.left = self._left_rotate(node.left)
                self.metrics.rotations += 2
                return self._right_rotate(node)

        if balance < -1:
            if self._get_balance(node.right) <= 0:
                self.metrics.rotations += 1
                return self._left_rotate(node)
            else:
                node.right = self._right_rotate(node.right)
                self.metrics.rotations += 2
                return self._left_rotate(node)

        return node

    # ----------------- Rotações e Auxiliares -----------------
    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _min(self, node):
        while node.left:
            node = node.left
        return node

    def search(self, id):
        return self._search(self.root, id)

    def _search(self, node, id):
        if not node: return None
        self.metrics.comparisons += 1
        if id == node.id: return node
        elif id < node.id: return self._search(node.left, id)
        else: return self._search(node.right, id)

    def height(self):
        return self._get_height(self.root)
    
    def count_nodes(self):
        return self.metrics.nodes

    def reset_metrics(self):
        self.metrics.reset()