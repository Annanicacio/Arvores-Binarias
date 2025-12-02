# metrics.py
# Este arquivo contém funções utilitárias usadas por todas as árvores,

class Metrics:
    """Armazena métricas de operação das árvores."""
    def __init__(self):
        self.rotations = 0
        self.comparisons = 0
        self.nodes = 0

    def reset(self):
        self.rotations = 0
        self.comparisons = 0
        self.nodes = 0
