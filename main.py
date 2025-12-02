# main.py
import time
import sys
from generator import gerar_dados
from bst import BST
from avl import AVL
from rbt import RedBlackTree

# Aumenta o limite de recursão para suportar árvores grandes
sys.setrecursionlimit(20000)

def testar_arvore(ArvoreClass, elementos, nome_arvore):
    arvore = ArvoreClass()
    arvore.reset_metrics()
    n = len(elementos)
    
    # ----------------- Inserção -----------------
    start = time.time()
    for e in elementos:
        arvore.insert(*e)
    end = time.time()
    tempo_insercao = (end - start) * 1000  # ms
    
    altura_final = arvore.height()
    rotacoes = arvore.metrics.rotations
    comparacoes_ins = arvore.metrics.comparisons
    
    # ----------------- Busca -----------------
    arvore.metrics.comparisons = 0 
    start = time.time()
    for e in elementos:
        arvore.search(e[0])
    end = time.time()
    tempo_busca = (end - start) * 1000  # ms
    comparacoes_busca = arvore.metrics.comparisons

    # ----------------- Remoção -----------------
    arvore.metrics.comparisons = 0 
    arvore.metrics.rotations = 0   
    
    start = time.time()
    for e in elementos:
        arvore.delete(e[0])
    end = time.time()
    tempo_remocao = (end - start) * 1000  # ms
    comparacoes_rem = arvore.metrics.comparisons
    rotacoes_rem = arvore.metrics.rotations

    # Resultados formatados
    resultado = {
        "Altura Final": altura_final,
        "Tempo Inserção (ms)": f"{tempo_insercao:.2f}",
        "Tempo Busca (ms)": f"{tempo_busca:.2f}",
        "Tempo Remoção (ms)": f"{tempo_remocao:.2f}",
        "Rotações (Total)": rotacoes + rotacoes_rem,
        "Média Comp. Inserção": f"{comparacoes_ins / n:.2f}",
        "Média Comp. Busca": f"{comparacoes_busca / n:.2f}"
    }
    return resultado

def main():
    tamanhos = [100, 1000, 10000]

    for n in tamanhos:
        print("\n" + "=" * 100)
        print(f" TESTANDO COM {n} ELEMENTOS".center(100))
        print("=" * 100)
        
        elementos = gerar_dados(n)
        classes = [("BST", BST), ("AVL", AVL), ("RBT", RedBlackTree)]
        
        resultados_finais = []

        for nome, Classe in classes:
            try:
                # Copia lista para garantir dados iguais
                dados_teste = list(elementos)
                res = testar_arvore(Classe, dados_teste, nome)
                res["Algoritmo"] = nome
                resultados_finais.append(res)
            except Exception as e:
                print(f"Erro ao testar {nome}: {e}")

        # --- EXIBIR TABELA ---
        headers = [
            "Algoritmo", "Tempo Ins(ms)", "Tempo Bus(ms)", "Tempo Rem(ms)", 
            "Altura", "Rot. Total", "Med Comp Ins", "Med Comp Bus"
        ]
        
        # Formatação da tabela
        row_format = "{:<10} | {:<13} | {:<13} | {:<13} | {:<8} | {:<10} | {:<12} | {:<12}"
        
        print(row_format.format(*headers))
        print("-" * 115)

        for r in resultados_finais:
            print(row_format.format(
                r["Algoritmo"],
                r["Tempo Inserção (ms)"],
                r["Tempo Busca (ms)"],
                r["Tempo Remoção (ms)"],
                r["Altura Final"],
                r["Rotações (Total)"],
                r["Média Comp. Inserção"],
                r["Média Comp. Busca"]
            ))
        print("-" * 115)

if __name__ == "__main__":
    main()