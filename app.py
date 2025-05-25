from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import uuid
import os
from jogador_analyzer import JogadorAnalyzer

app = Flask(__name__)

arquivos = [
    "atacantes.csv",
    "goleiros.csv",
    "laterais.csv",
    "zagueiros.csv",
    "volantes.csv",
    "boxtobox.csv",
    "armadores.csv"
]

analise = JogadorAnalyzer(arquivos)
nacionalidades = analise.get_nacionalidades()
caracteristicas = analise.get_caracteristicas()
nomes_jogadores = analise.get_nomes_jogadores()

@app.route("/")
def index():
    return render_template("index.html",
                           caracteristicas=caracteristicas,
                           nomes_jogadores=nomes_jogadores,
                           nacionalidades=nacionalidades,
                           caracteristicas_selecionadas=[])

@app.route("/filtrar", methods=["POST"])
def filtrar():
    posicao = request.form.get("posicao")
    valor = request.form.get("valor")
    carac1 = request.form.get("carac1")
    carac2 = request.form.get("carac2")
    idade= request.form.get("idade")
    nome= request.form.get("nome")
    nacionalidade = request.form.get("nacionalidade")

    # Remover redirecionamento automático para página do jogador para evitar ir direto
    # Apenas filtra e exibe lista com resultados

    try:
        valor = float(valor) if valor else None
    except ValueError:
        valor = None

    try:
        idade = int(idade) if idade else None
    except ValueError:
        idade = None

    caracs = [c for c in [carac1, carac2] if c]
    resultado = analise.filtrar_jogadores(posicao, valor, caracs, idade=idade, nome=nome, nacionalidade=nacionalidade)

    return render_template("index.html",
                           tabela=resultado.to_dict(orient="records"),
                           caracteristicas=caracteristicas,
                           nomes_jogadores=nomes_jogadores,
                           nacionalidades=nacionalidades,
                           caracteristicas_selecionadas=caracs)

@app.route("/comparar", methods=["POST"])
def comparar():
    nome1 = request.form.get("jogador1")
    nome2 = request.form.get("jogador2")

    j1, j2 = analise.comparar_jogadores(nome1, nome2)
    if j1 is None or j2 is None:
        return "Jogador não encontrado.", 400

    comparacao = pd.DataFrame({
        "Caracteristica": caracteristicas,
        nome1: j1[caracteristicas].values,
        nome2: j2[caracteristicas].values
    })

    imagem = analise.grafico_jogadores(nome1, nome2)

    return render_template("comparacao.html", comparacao=comparacao.to_dict(orient="records"), nome1=nome1, nome2=nome2, imagem=imagem)

@app.route('/jogador')
def jogador():
    nome = request.args.get('nome')
    posicao = request.args.get('posicao')

    if not nome or not posicao:
        return "Parâmetros 'nome' e 'posicao' são obrigatórios."

    df = analise.dataframes.get(posicao)
    if df is not None and nome in df['Nome'].values:
        dados_jogador = df[df['Nome'] == nome].iloc[0]

        caracteristicas = [c for c in analise.get_caracteristicas() if c in dados_jogador.index]
        dados_grafico = {carac: dados_jogador[carac] for carac in caracteristicas}

        if not dados_grafico:
            return "Nenhuma característica válida encontrada para esse jogador."

        nome_arquivo = f"grafico_{uuid.uuid4().hex}.png"
        caminho_arquivo = os.path.join('static', nome_arquivo)

        plt.figure(figsize=(10, 5))
        fig = plt.gcf()
        fig.patch.set_alpha(0.0)  # Fundo transparente

        nomes = list(dados_grafico.keys())
        valores = list(dados_grafico.values())

        plt.bar(nomes, valores, color='royalblue', width=0.5)

        limite_superior = max(valores) * 1.15
        plt.ylim(0, limite_superior)

        for i, valor in enumerate(valores):
            plt.text(i, valor + limite_superior * 0.015, f'{valor:.2f}', ha='center', fontsize=10, color='white')

        plt.xticks(rotation=45, color='white')  # Nomes das estatísticas em branco
        plt.yticks(color='white')                # Números do eixo y em branco

        ax = plt.gca()
        for spine in ax.spines.values():         # Borda branca
            spine.set_color('white')

        ax.tick_params(axis='x', colors='white')  # Ticks eixo X em branco (linha pequena)
        ax.tick_params(axis='y', colors='white')  # Ticks eixo Y em branco

        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig(caminho_arquivo, transparent=True)
        plt.close()

        return render_template('jogador.html', info=dados_jogador, imagem_grafico=nome_arquivo)
    else:
        return f"Jogador '{nome}' não encontrado na posição '{posicao}'."

if __name__ == "__main__":
    app.run(debug=True)
