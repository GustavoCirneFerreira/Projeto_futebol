import matplotlib.pyplot as plt

def gerar_grafico(dados):
    nomes = list(dados.keys())
    valores = list(dados.values())

    plt.figure(figsize=(8, 4))
    barras = plt.bar(nomes, valores, color='royalblue')

    for i, valor in enumerate(valores):
        plt.text(i, valor + max(valores) * 0.03, f'{valor}', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('static/grafico.png')
    plt.close()
