import matplotlib.pyplot as plt

def gerar_grafico(dados):
    if not dados:
        print("[AVISO] Nenhum dado fornecido para o gráfico.")
        return

    nomes = list(dados.keys())
    valores = list(dados.values())

    plt.figure(figsize=(10, 5))
    barras = plt.bar(nomes, valores, color='royalblue')

    for i, valor in enumerate(valores):
        plt.text(i, valor + max(valores) * 0.03, f'{valor:.2f}', ha='center', fontsize=9)

    plt.xticks(rotation=30, ha='right', fontsize=9)
    plt.yticks(fontsize=9)
    plt.title("Estatísticas do Jogador", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('static/grafico.png', transparent=True)
    plt.close()
