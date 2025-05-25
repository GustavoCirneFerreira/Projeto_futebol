from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from jogador_analyzer import JogadorAnalyzer
import uuid
import os


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

    # Se o usuário digitou o nome do jogador, tentar redirecionar para a página individual
    if nome and nome.strip() != "":
        if posicao == "Todas":
            for pos, df in analise.dataframes.items():
                if nome in df["Nome"].values:
                    return redirect(url_for("jogador", nome=nome, posicao=pos))
        else:
            df = analise.dataframes.get(posicao)
            if df is not None and nome in df["Nome"].values:
                return redirect(url_for("jogador", nome=nome, posicao=posicao))

    # Continua com filtro normal caso não tenha nome ou jogador não encontrado
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

    df = analise.dataframes.get(posicao)
    if df is not None and nome in df['Nome'].values:
        dados_jogador = df[df['Nome'] == nome].iloc[0]

        # Filtra características que existem para esse jogador
        caracteristicas = [c for c in analise.get_caracteristicas() if c in dados_jogador.index]
        dados_grafico = {carac: dados_jogador[carac] for carac in caracteristicas}

        # Gera nome único para o gráfico
        nomearquivo = f"grafico{uuid.uuid4().hex}.png"
        caminho_arquivo = os.path.join('static', nomearquivo)

        # Criação do gráfico com fundo transparente real
        plt.figure(figsize=(10, 5))
        fig = plt.gcf()
        fig.patch.set_alpha(0.0)  # Fundo da figura transparente

        nomes = list(dados_grafico.keys())
        valores = list(dados_grafico.values())

        barras = plt.bar(nomes, valores, color='royalblue', width=0.5)

        limite_superior = max(valores) * 1.15
        plt.ylim(0, limite_superior)

        for i, valor in enumerate(valores):
            plt.text(i, valor + limite_superior * 0.015, f'{valor:.2f}', ha='center', fontsize=10)

        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig(caminho_arquivo, transparent=True)
        plt.close()

        return render_template('jogador.html', info=dados_jogador, imagem_grafico=nomearquivo)
    else:
        return f"Jogador '{nome}' não encontrado na posição '{posicao}'."
    
if __name__ == "__main__":
    app.run(debug=True)
