# generator.py
import random
import string

def gerar_dados(n):
    """
    Gera uma lista de elementos (id, name, extra) aleatórios.
    Os IDs são embaralhados para evitar o pior caso da BST (lista ligada).
    """
    ids = list(range(1, n + 1))
    random.shuffle(ids)  # CRUCIAL: Embaralha para evitar pior caso da BST
    
    elementos = []
    for id_val in ids:
        name = ''.join(random.choices(string.ascii_letters, k=5))
        extra = random.randint(1, 100)
        elementos.append((id_val, name, extra))
    return elementos