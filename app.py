# import app
from flask import Flask, render_template, request
import pandas as pd
from jogador_analyzer import JogadorAnalyzer

app = Flask(__name__)

# Arquivos de entrada
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

    # Características numéricas comuns
    num1 = j1.to_frame().T.select_dtypes(include='number')
    num2 = j2.to_frame().T.select_dtypes(include='number')

    caracteristicas_comuns = [col for col in num1.index if col in num2.index and 
                              col not in ['Idade', 'Salário']]


    comparacao = pd.DataFrame({
        "Caracteristica": caracteristicas_comuns,
        nome1: [j1[col].item() for col in caracteristicas_comuns],
        nome2: [j2[col].item() for col in caracteristicas_comuns]
    })

    imagem = analise.grafico_jogadores(nome1, nome2)

    return render_template("comparacao.html", comparacao=comparacao.to_dict(orient="records"), nome1=nome1, nome2=nome2
                           , imagem=imagem)


if __name__ == "__main__":  
    app.run(debug=True)
