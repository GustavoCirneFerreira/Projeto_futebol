# Importa o Flask e funções para renderizar HTML, lidar com formulários e redirecionar rotas
from flask import Flask, render_template, request, redirect, url_for
# Pandas para análise de dados
import pandas as pd
# Define o backend do matplotlib como "Agg" (evita o uso de interface gráfica como Tkinter)
import matplotlib
matplotlib.use("Agg")  # ⬅️ Garante que plt.savefig funcione sem erro de thread
import matplotlib.pyplot as plt
# Gera identificadores únicos para nomear arquivos de gráfico
import uuid
# Acesso ao sistema de arquivos
import os
# Classe personalizada que gerencia os dados dos jogadores
from jogador_analyzer import JogadorAnalyzer

# Cria a instância principal da aplicação Flask
app = Flask(__name__) 

# Carrega os dados e prepara análises
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
    # Coleta os dados do formulário
    posicao = request.form.get("posicao")
    valor = request.form.get("valor")
    carac1 = request.form.get("carac1")
    carac2 = request.form.get("carac2")
    idade = request.form.get("idade")
    nome = request.form.get("nome")
    nacionalidade = request.form.get("nacionalidade")

    # Converte valor e idade se forem válidos
    try: valor = float(valor) if valor else None
    except ValueError: valor = None

    try: idade = int(idade) if idade else None
    except ValueError: idade = None

    # Junta características selecionadas
    caracs = [c for c in [carac1, carac2] if c]

    # Aplica o filtro usando o JogadorAnalyzer
    resultado = analise.filtrar_jogadores(posicao, valor, caracs, idade, nome, nacionalidade)

    # Renderiza os resultados na mesma página inicial
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

    # Compara jogadores
    j1, j2 = analise.comparar_jogadores(nome1, nome2)
    if j1 is None or j2 is None:
        return "Jogador não encontrado.", 400

    # Cria DataFrame para exibir comparação
    comparacao = pd.DataFrame({
        "Caracteristica": caracteristicas,
        nome1: j1[caracteristicas].values,
        nome2: j2[caracteristicas].values
    })

    # Detecta posição de cada jogador para links clicáveis
    df = analise.df_total
    pos1 = df[df['Nome'] == nome1]['Posição'].values[0]
    pos2 = df[df['Nome'] == nome2]['Posição'].values[0]

    # Gera gráfico em base64
    imagem = analise.grafico_jogadores(nome1, nome2)

    # Renderiza o template de comparação
    return render_template("comparacao.html",
                            comparacao=comparacao.to_dict(orient="records"),
                            nome1=nome1, nome2=nome2,
                            pos1=pos1, pos2=pos2,
                            imagem=imagem)


@app.route('/jogador')
def jogador():
    nome = request.args.get('nome')
    posicao = request.args.get('posicao')

    if not nome or not posicao:
        return "Parâmetros 'nome' e 'posicao' são obrigatórios."

    # Busca o dataframe correspondente à posição
    df = analise.dataframes.get(posicao)
    if df is not None and nome in df['Nome'].values:
        dados_jogador = df[df['Nome'] == nome].iloc[0]

        # Filtra as características disponíveis para aquele jogador
        caracteristicas = [c for c in analise.get_caracteristicas() if c in dados_jogador.index]
        dados_grafico = {carac: dados_jogador[carac] for carac in caracteristicas}

        if not dados_grafico:
            return "Nenhuma característica válida encontrada para esse jogador."

        # Gera gráfico
        nome_arquivo = f"grafico_{uuid.uuid4().hex}.png"
        caminho_arquivo = os.path.join('static', nome_arquivo)

        # Cria gráfico com matplotlib
        plt.figure(figsize=(10, 5))
        fig = plt.gcf()
        fig.patch.set_alpha(0.0)  # fundo transparente

        nomes = list(dados_grafico.keys())
        valores = list(dados_grafico.values())

        plt.bar(nomes, valores, color='royalblue', width=0.5)
        limite_superior = max(valores) * 1.15
        plt.ylim(0, limite_superior)

        for i, valor in enumerate(valores):
            plt.text(i, valor + limite_superior * 0.015, f'{valor:.2f}', ha='center', fontsize=10, color='white')

        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        ax = plt.gca()
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig(caminho_arquivo, transparent=True)
        plt.close()

        return render_template('jogador.html', info=dados_jogador, imagem_grafico=nome_arquivo)
    else:
        return f"Jogador '{nome}' não encontrado na posição '{posicao}'."

if __name__ == "__main__":
    app.run(debug=True) # Inicia o servidor Flask com debug ativado