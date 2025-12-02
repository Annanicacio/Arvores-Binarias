# bst.py
from metrics import Metrics

class BSTNode:
    def __init__(self, id, name, extra=None):
        self.id = id
        self.name = name
        self.extra = extra
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
        self.metrics = Metrics()

    # ----------------- Inserção -----------------
    def insert(self, id, name, extra=None):
        self.root = self._insert(self.root, id, name, extra)
        self.metrics.nodes += 1

    def _insert(self, node, id, name, extra):
        if node is None:
            return BSTNode(id, name, extra)
        
        self.metrics.comparisons += 1
        if id < node.id:
            node.left = self._insert(node.left, id, name, extra)
        else:
            node.right = self._insert(node.right, id, name, extra)
        return node

    # ----------------- Busca -----------------
    def search(self, id):
        return self._search(self.root, id)

    def _search(self, node, id):
        if node is None:
            return None
        
        self.metrics.comparisons += 1
        if id == node.id:
            return node
        elif id < node.id:
            return self._search(node.left, id)
        else:
            return self._search(node.right, id)

    # ----------------- Remoção -----------------
    def delete(self, id):
        self.root = self._delete(self.root, id)

    def _delete(self, node, id):
        if node is None:
            return None
        
        self.metrics.comparisons += 1
        if id < node.id:
            node.left = self._delete(node.left, id)
        elif id > node.id:
            node.right = self._delete(node.right, id)
        else:
            # Nó encontrado
            self.metrics.nodes -= 1
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            temp = self._min(node.right)
            node.id, node.name, node.extra = temp.id, temp.name, temp.extra
            self.metrics.nodes += 1 # Compensa o decremento da recursão abaixo
            node.right = self._delete(node.right, temp.id)
            
        return node

    def _min(self, node):
        while node.left:
            node = node.left
        return node

    # ----------------- Traversals (Obrigatórios) -----------------
    def inorder(self):
        r = []
        self._inorder(self.root, r)
        return r

    def _inorder(self, node, r):
        if node:
            self._inorder(node.left, r)
            r.append(node.id)
            self._inorder(node.right, r)

    def preorder(self):
        r = []
        self._preorder(self.root, r)
        return r

    def _preorder(self, node, r):
        if node:
            r.append(node.id)
            self._preorder(node.left, r)
            self._preorder(node.right, r)

    def postorder(self):
        r = []
        self._postorder(self.root, r)
        return r

    def _postorder(self, node, r):
        if node:
            self._postorder(node.left, r)
            self._postorder(node.right, r)
            r.append(node.id)

    # ----------------- Métricas -----------------
    def height(self):
        def _h(node):
            if node is None: return 0
            return 1 + max(_h(node.left), _h(node.right))
        return _h(self.root)

    def count_nodes(self):
        return self.metrics.nodes

    def reset_metrics(self):
        self.metrics.reset()