# Importa o módulo de plotagem do matplotlib
import matplotlib.pyplot as plt

# Define uma função chamada gerar_grafico, que recebe um dicionário dados contendo pares nome:valor.
def gerar_grafico(dados):
    # Se o dicionário estiver vazio ou for None, exibe uma mensagem e interrompe a execução da função.
    if not dados:
        print("[AVISO] Nenhum dado fornecido para o gráfico.")
        return

    # Extrai as chaves (nomes das características) e os valores numéricos do dicionário.
    nomes = list(dados.keys())
    valores = list(dados.values())

    # Cria uma nova figura para o gráfico com tamanho 10x5 polegadas.
    plt.figure(figsize=(10, 5))
    # Cria um gráfico de barras verticais com cor azul para cada característica.
    barras = plt.bar(nomes, valores, color='royalblue')

    # Para cada barra, escreve o valor numérico acima dela, com espaçamento proporcional.
    for i, valor in enumerate(valores):
        plt.text(i, valor + max(valores) * 0.03, f'{valor:.2f}', ha='center', fontsize=9)

    plt.xticks(rotation=30, ha='right', fontsize=9) # Roda os rótulos do eixo X (nomes das características) em 30° para melhor leitura.
    plt.yticks(fontsize=9) # Define o tamanho da fonte dos números do eixo Y.
    plt.title("Estatísticas do Jogador", fontsize=12) # Adiciona um título ao gráfico.
    plt.grid(axis='y', linestyle='--', alpha=0.3) # Adiciona linhas de grade horizontais para facilitar a leitura dos valores.
    plt.tight_layout() # Ajusta automaticamente os elementos do gráfico para que não fiquem cortados.
    plt.savefig('static/grafico.png', transparent=True) # Salva o gráfico como imagem .png na pasta static, com fundo transparente.
    plt.close() # Fecha o gráfico para liberar memória (importante ao gerar vários gráficos em sequência).
