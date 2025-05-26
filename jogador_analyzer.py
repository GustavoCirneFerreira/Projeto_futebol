import chardet
import pandas as pd
import re
import matplotlib.pyplot as plt
import io
import base64


# Gerencia todos os dados dos jogadores, incluindo carregamento, limpeza, filtragem e gráficos.
class JogadorAnalyzer:
    # Corrige e converte oq está errado, e armazenatudo em um grande dataframe
    def __init__(self, arquivos):
        self.dfs = []
        self.dataframes = {}

        for arq in arquivos:
            try:
                posicao = arq.split("/")[-1].replace(".csv", "")
                
                # Detectar o encoding correto do arquivo

                df = pd.read_csv(arq, encoding="utf-8", sep=";")


                # Converte os nomes escritos errados no CSV em corretos
                df.columns = df.columns.str.replace("SalÃ¡rio", "Salário")
                df.columns = df.columns.str.replace("PressÃ£o tentadas", "Pressão tentadas")
                df["Valor Estimado"] = df["Valor Estimado"].str.replace("N�o est� � venda", "Não está à venda")
                df["Nome"] = df["Nome"].replace({"Vitor Gon�alves": "Vitor Gonçalves"})
                df["Nome"] = df["Nome"].replace({"Jo�o Artur": "João Artur"})
                df["Nome"] = df["Nome"].replace({"Jo�o Victor Silva": "João Victor Silva"})
                df["Nome"] = df["Nome"].replace({"Jo�o Louren�o": "João Lourenço"})
                df["Nome"] = df["Nome"].replace({"David Kau�": "David Kauã"})
                df["Nome"] = df["Nome"].replace({"Werik Pop�": "Werik Popó"})
                df["Nome"] = df["Nome"].replace({"Andr� Luiz": "André Luiz"})
                df["Nome"] = df["Nome"].replace({"Kek�": "Keké"})
                df["Nome"] = df["Nome"].replace({"St�nio": "Stênio"})
                df["Nome"] = df["Nome"].replace({"Jo�o Carlos": "João Carlos"})
                df["Nome"] = df["Nome"].replace({"Emiliano Rodr�guez": "Emiliano Rodríguez"})
                df["Nome"] = df["Nome"].replace({"Romeo Ben�tez": "Romeo Benítez"})
                df["Nome"] = df["Nome"].replace({"Eli�dson": "Eliédson"})
                df["Nome"] = df["Nome"].replace({"Z� Hugo": "Zé Hugo"})
                df["Nome"] = df["Nome"].replace({"Z� Phelipe": "Zé Phelipe"})
                df["Nome"] = df["Nome"].replace({"L�o Gon�alves": "Léo Gonçalves"})
                df["Nome"] = df["Nome"].replace({"L�o Santos": "Léo Santos"})
                df["Nome"] = df["Nome"].replace({"�verton Galdino": "Éverton Galdino"})
                df["Nome"] = df["Nome"].replace({"Mat�as Segovia": "Matías Segovia"})
                df["Nome"] = df["Nome"].replace({"R�mulo Cardoso": "Rômulo Cardoso"})
                df["Nome"] = df["Nome"].replace({"Jo�o Dalla Corte": "João Dalla Corte"})
                df["Nome"] = df["Nome"].replace({"Matheus Gon�alves": "Matheus Gonçalves"})
                df["Nome"] = df["Nome"].replace({"Andr� Henrique": "André Henrique"})
                df["Nome"] = df["Nome"].replace({"Matheus Dav�": "Matheus Davó"})
                df["Nome"] = df["Nome"].replace({"L�o Mana": "Léo Mana"})
                df["Nome"] = df["Nome"].replace({"Jos� Breno": "José Breno"})
                df["Nome"] = df["Nome"].replace({"Mateus Gon�alves": "Mateus Gonçalves"})
                df["Nome"] = df["Nome"].replace({"Lel�": "Lelê"})
                df["Nome"] = df["Nome"].replace({"Higor Merit�o": "Higor Meritão"})
                df["Nome"] = df["Nome"].replace({"Rafael Rat�o": "Rafael Ratão"})
                df["Nome"] = df["Nome"].replace({"Oct�vio": "Octávio"})
                df["Nome"] = df["Nome"].replace({"Ca�que Gon�alves": "Caíque Gonçalves"})
                df["Nome"] = df["Nome"].replace({"Andr� Luis": "André"})
                df["Nome"] = df["Nome"].replace({"Guilherme Rom�o": "Guilherme Romão"})
                df["Nome"] = df["Nome"].replace({"L�o Gomes": "Léo Gomes"})
                df["Nome"] = df["Nome"].replace({"Z� Guilherme": "Zé Guilherme"})
                df["Nome"] = df["Nome"].replace({"R�mulo": "Rômulo"})
                df["Nome"] = df["Nome"].replace({"Ata�de": "Ataíde"})
                df["Nome"] = df["Nome"].replace({"F�bio Matheus": "Fábio Matheus"})
                df["Nome"] = df["Nome"].replace({"Nik�o": "Nikão"})
                df["Nome"] = df["Nome"].replace({"Nen�": "Nenê"})
                df["Nome"] = df["Nome"].replace({"Michel Ara�jo": "Michel Araújo"})
                df["Nome"] = df["Nome"].replace({"Z� Welison": "Zé Welison"})
                df["Nome"] = df["Nome"].replace({"Maur�cio": "Maurício"})
                df["Nome"] = df["Nome"].replace({"Vinicius Kau�": "Vinicius Kauã"})
                df["Nome"] = df["Nome"].replace({"Rom�rcio": "Romércio"})
                df["Nome"] = df["Nome"].replace({"Wilker �ngel": "Wilker Ângel"})
                df["Nome"] = df["Nome"].replace({"Yuli�n G�mez": "Yuliãn Gómez"})
                df["Nome"] = df["Nome"].replace({"Matheus Bel�m": "Matheus Belém"})
                df["Nome"] = df["Nome"].replace({"Z� Gabriel": "Zé Gabriel"})
                df["Nome"] = df["Nome"].replace({"J�dson": "Jádson"})
                df["Nome"] = df["Nome"].replace({"Du Queir�z": "Du Queiróz"})
                df["Nome"] = df["Nome"].replace({"Igor Cari�s": "Igor Cariús"})
                df["Nome"] = df["Nome"].replace({"Ra�": "Raí"})
                df["Nome"] = df["Nome"].replace({"Jhoanner Ch�vez": "Jhoanner Chávez"})
                df["Nome"] = df["Nome"].replace({"F�bio Soares": "Fábio Soares"})
                df["Nome"] = df["Nome"].replace({"Jo�o Lucas": "João Lucas"})
                df["Nome"] = df["Nome"].replace({"Geuv�nio": "Geuvânio"})
                df["Nome"] = df["Nome"].replace({"C�sar Haydar": "César Haydar"})
                df["Nome"] = df["Nome"].replace({"H�rcules": "Hércules"})
                df["Nome"] = df["Nome"].replace({"J�nior Santos": "Júnior Santos"})
                df["Nome"] = df["Nome"].replace({"Cac�": "Cacá"})
                df["Nome"] = df["Nome"].replace({"Andr�s Roa": "Andrés Roa"})
                df["Nome"] = df["Nome"].replace({"Z� Ivaldo": "Zé Ivaldo"})
                df["Nome"] = df["Nome"].replace({"Juan Mart�n Lucero": "Juan Martín Lucero"})
                df["Nome"] = df["Nome"].replace({"Pep�": "Pepê"})
                df["Nome"] = df["Nome"].replace({"Jo�o Pedro": "João Pedro"})
                df["Nome"] = df["Nome"].replace({"Jaj�": "Jajá"})
                df["Nome"] = df["Nome"].replace({"Dami�n Bobadilla": "Damián Bobadilha"})
                df["Nome"] = df["Nome"].replace({"Ka�que Rocha": "Kaíque Rocha"})
                df["Nome"] = df["Nome"].replace({"Ja�lson": "Jaílson"})
                df["Nome"] = df["Nome"].replace({"L�o Natel": "Léo Natel"})
                df["Nome"] = df["Nome"].replace({"�lvaro Barreal": "Álvaro Barrel"})
                df["Nome"] = df["Nome"].replace({"Jos� Manuel L�pez": "José Manuel López"})
                df["Nome"] = df["Nome"].replace({"Victor Lu�s": "Victor Luís"})
                df["Nome"] = df["Nome"].replace({"Bruno Tubar�o": "Bruno Tubarão"})
                df["Nome"] = df["Nome"].replace({"Tom�s Pochettino": "Tomás Pochettino"})
                df["Nome"] = df["Nome"].replace({"Tom�s Cardona": "Tomás Cardona"})
                df["Nome"] = df["Nome"].replace({"Matheus Ara�jo": "Matheus Araújo"})
                df["Nome"] = df["Nome"].replace({"�ngel Romero": "Ângel Romero"})
                df["Nome"] = df["Nome"].replace({"Lu�s Oyama": "Luís Oyama"})
                df["Nome"] = df["Nome"].replace({"Ant�nio Carlos": "Antônio Carlos"})
                df["Nome"] = df["Nome"].replace({"Fabr�cio Bruno": "Fabrício Bruno"})
                df["Nome"] = df["Nome"].replace({"Z� Rafael": "Zé Rafael"})
                df["Nome"] = df["Nome"].replace({"Kau�": "Kauã"})
                df["Nome"] = df["Nome"].replace({"Germ�n Cano": "Germán Cano"})
                df["Nome"] = df["Nome"].replace({"L�o": "Léo"})
                df["Nome"] = df["Nome"].replace({"Yony Gonz�lez": "Yony González"})
                df["Nome"] = df["Nome"].replace({"Ra�l C�ceres": "Rafael Cáceres"})
                df["Nome"] = df["Nome"].replace({"Victor S�": "Victor Sá"})
                df["Nome"] = df["Nome"].replace({"Emanuel Br�tez": "Emanuel Brítez"})
                df["Nome"] = df["Nome"].replace({"Luiz Ara�jo": "Luiz Araújo"})
                df["Nome"] = df["Nome"].replace({"Jo�o Marcelo": "João Marcelo"})
                df["Nome"] = df["Nome"].replace({"�scar Estupi��n": "Óscar Estupriñá"})
                df["Nome"] = df["Nome"].replace({"L�o Pereira": "Léo Pereira"})
                df["Nome"] = df["Nome"].replace({"Jes�": "Jesé"})
                df["Nome"] = df["Nome"].replace({"Emerson J�nior": "Emerson Júnior"})
                df["Nome"] = df["Nome"].replace({"Luan C�ndido": "Luan Cândido"})
                df["Nome"] = df["Nome"].replace({"N�ris": "Néris"})
                df["Nome"] = df["Nome"].replace({"Mat�as Rojas": "Matias Rojas"})
                df["Nome"] = df["Nome"].replace({"Luc�o": "Lucão"})
                df["Nome"] = df["Nome"].replace({"Richard R�os": "Richard Ríos"})
                df["Nome"] = df["Nome"].replace({"L�o Ortiz": "Léo Ortiz"})
                df["Nome"] = df["Nome"].replace({"Ot�vio": "Otávio"})
                df["Nome"] = df["Nome"].replace({"Eden�lson": "Edenílson"})
                df["Nome"] = df["Nome"].replace({"L�zaro": "Lázaro"})
                df["Nome"] = df["Nome"].replace({"Alem�o": "Alemão"})
                df["Nome"] = df["Nome"].replace({"Ren�": "Renê"})
                df["Nome"] = df["Nome"].replace({"Cristian Pav�n": "Cristian Pávon"})
                df["Nome"] = df["Nome"].replace({"Jos� Luis Rodr�guez": "José Luís Rodríguez"})
                df["Nome"] = df["Nome"].replace({"Andr� Ramalho": "André Ramalho"})
                df["Nome"] = df["Nome"].replace({"L�o Linck": "Léo Linick"})
                df["Nome"] = df["Nome"].replace({"An�bal Moreno": "Aníbal Moreno"})
                df["Nome"] = df["Nome"].replace({"Jo�o Ricardo": "João Ricardo"})
                df["Nome"] = df["Nome"].replace({"Andr�": "André"})
                df["Nome"] = df["Nome"].replace({"Vit�o": "Vitão"})
                df["Nome"] = df["Nome"].replace({"Jos� Hurtado": "José Hurtado"})
                df["Nome"] = df["Nome"].replace({"Jimmy Mart�nez": "Jimmy Martínez"})
                df["Nome"] = df["Nome"].replace({"Benjam�n Kuscevic": "Benjamín Kuscevic"})
                df["Nome"] = df["Nome"].replace({"Mat�as Zaracho": "Matías Zaracho"})
                df["Nome"] = df["Nome"].replace({"Mar�al": "Marçal"})
                df["Nome"] = df["Nome"].replace({"Agust�n Canobbio": "Agustín Canobbio"})
                df["Nome"] = df["Nome"].replace({"F�lix Torres": "Félix Torres"})
                df["Nome"] = df["Nome"].replace({"Nicol�s de la Cruz": "Nicolás de la Cruz"})
                df["Nome"] = df["Nome"].replace({"V�ctor Cuesta": "Victor Cuesta"})
                df["Nome"] = df["Nome"].replace({"Maur�cio Ant�nio": "Maurício Antônio "})
                df["Nome"] = df["Nome"].replace({"Cristi�n Zapata": "Cristián Zapata"})
                df["Nome"] = df["Nome"].replace({"F�gner": "Fágner"})
                df["Nome"] = df["Nome"].replace({"Jos� Cifuentes": "José Cifuentes"})
                df["Nome"] = df["Nome"].replace({"Agust�n Rossi": "Agustín Rossi"})
                df["Nome"] = df["Nome"].replace({"F�bio": "Fábio"})
                df["Nome"] = df["Nome"].replace({"Jo�o Victor": "João Victor"})
                df["Nome"] = df["Nome"].replace({"Math�as Villasanti": "Mathías Vilasanti"})
                df["Nome"] = df["Nome"].replace({"V�tor Hugo": "Víctor Hugo"})
                df["Nome"] = df["Nome"].replace({"Mat�as Vi�a": "Matías Viña"})
                df["Nome"] = df["Nome"].replace({"L�o Jardim": "Léo Jardim"})
                df["Nome"] = df["Nome"].replace({"Dami�n Su�rez": "Damián Suárez"})
                df["Nome"] = df["Nome"].replace({"C�ssio": "Cássio"})
                df["Nome"] = df["Nome"].replace({"Gustavo G�mez": "Gustavo Goméz"})
                df["Nome"] = df["Nome"].replace({"Rafael Santos Borr�": "Rafael Santos Borré"})
                df["Nome"] = df["Nome"].replace({"G�rson": "Gérson"})
                df["Nome"] = df["Nome"].replace({"D�ria": "Dória"})
                df["Nome"] = df["Nome"].replace({"Gatito Fern�ndez": "Gatito Fernández"})
                df["Nome"] = df["Nome"].replace({"Joaqu�n Piquerez": "Joaquín Piquerez"})
                df["Nome"] = df["Nome"].replace({"Agust�n Marches�n": "Agustín Marchesín"})
                df["Nome"] = df["Nome"].replace({"James Rodr�guez": "James Rodríguez"})
                df["Nome"] = df["Nome"].replace({"Charles Ar�nguiz": "Charles Aránguiz"})


                # Adiciona coluna com a posição
                df["Posição"] = posicao

                # Mantém valor estimado original para exibição
                df["Valor Estimado Original"] = df["Valor Estimado"].copy()

                # Converte valor estimado para float para filtros
                df["Valor Estimado"] = df["Valor Estimado"].apply(self._converter_valor)

                # Converte salário para float
                if "Salário" not in df.columns:
                    df["Salário"] = 0
                else:
                    df["Salário"] = df["Salário"].apply(self._converter_salario)

                self.dfs.append(df)
                self.dataframes[posicao] = df

            except Exception as e:
                print(f"[ERRO] Falha ao carregar '{arq}': {e}")

        if self.dfs:
            self.df_total = pd.concat(self.dfs, ignore_index=True)
            self.df_total.fillna(0, inplace=True)
        else:
            self.df_total = pd.DataFrame()

    def _converter_valor(self, valor_str):
        """Converte valores como 'R$38M' ou 'Não está à venda' em float"""
        if not isinstance(valor_str, str):
            return 0

        if "Não está à venda" in valor_str:
            return 0

        match = re.search(r"R\$([\d,.]+)([MK]?)", valor_str.replace(".", ""))
        if match:
            valor = float(match.group(1).replace(",", "."))
            mult = match.group(2)
            # Multiplica por 1_000_000 se tiver M, ou 1_000 se tiver K
            if mult == "M":
                valor *= 1_000_000
            elif mult == "K":
                valor *= 1_000
            return valor

        return 0
    def _converter_salario(self, salario_str):
        """
        Converte salários do tipo "R$500K" ou "R$1.2M" em float.
        """
        if not isinstance(salario_str, str):
            return 0.0

        match = re.search(r"R\$([\d,.]+)([MK]?)", salario_str.replace(".", ""))
        if match:
            valor = float(match.group(1).replace(",", "."))
            mult = match.group(2)
            # Multiplica por 1_000_000 se tiver M, ou 1_000 se tiver K
            if mult == "M":
                valor *= 1_000_000
            elif mult == "K":
                valor *= 1_000
            return valor

        return 0.0

    # Retorna apenas colunas numéricas úteis (exclui Nome, Idade, etc).
    def get_caracteristicas(self):
        colunas_excluidas = [
            "Nome", "Posição", "Valor Estimado", "Clube",
            "Nac", "Pé Preferido", "Idade", "Expira", "Salário"
        ]
        return [col for col in self.df_total.columns if col not in colunas_excluidas and pd.api.types.is_numeric_dtype(self.df_total[col])]

    # Lista os nomes únicos dos jogadores.
    def get_nomes_jogadores(self):
        return self.df_total["Nome"].dropna().tolist()

    # Retorna todas as nacionalidades únicas.
    def get_nacionalidades(self):
        if "Nac" in self.df_total.columns:
            return sorted(self.df_total["Nac"].dropna().astype(str).unique().tolist())
        return []

    # Filtra jogadores e retorna o dataframe filtrado
    def filtrar_jogadores(self, posicao, valor=None, caracteristicas=None, idade=None, nome=None, nacionalidade=None):
        # Se tiver posição específica
        if posicao and posicao != "Todas":
            if posicao in self.dataframes:
                df = self.dataframes[posicao].copy()
            else:
                return pd.DataFrame()
        else:
            df = self.df_total.copy()

        # Filtro por nome
        if nome:
            df = df[df["Nome"].str.contains(nome, case=False, na=False)]

        # Filtro por idade
        if idade:
            df = df[df["Idade"] == idade]

        # Filtro por valor
        if valor:
            df = df[df["Valor Estimado"] <= valor]

        # Filtro por nacionalidade
        if nacionalidade and nacionalidade != "Todas":
            if "Nac" in df.columns:
                df = df[df["Nac"] == nacionalidade]
                

        # Ordenação pelas características escolhidas
        if caracteristicas:
            for carac in caracteristicas:
                if carac in df.columns:
                    df = df.sort_values(by=carac, ascending=False)

        return df

    # Retorna as linhas correspondentes aos dois jogadores escolhidos (ou None se não encontrados).
    def comparar_jogadores(self, nome1, nome2):
        df = self.df_total
        j1 = df[df["Nome"] == nome1]
        j2 = df[df["Nome"] == nome2]

        if j1.empty or j2.empty:
            return None, None

        return j1.iloc[0], j2.iloc[0]
    
    # Gera um gráfico comparando os dois jogadores
    def grafico_jogadores(self, nome1, nome2):
        df = self.df_total
        caracteristicas = self.get_caracteristicas()

        j1 = df[df["Nome"] == nome1]
        j2 = df[df["Nome"] == nome2]

        if j1.empty or j2.empty:
            print("Jogador não encontrado.")
            return None

        try:
            j1_dados = j1.iloc[0]
            j2_dados = j2.iloc[0]

            todas_caracteristicas = sorted(set(
                [c for c in caracteristicas if isinstance(j1_dados.get(c, 0), (int, float)) or isinstance(j2_dados.get(c, 0), (int, float))]
            ))

            if not todas_caracteristicas:
                print("⚠️ Nenhuma característica comparável encontrada.")
                return None

            dados_1 = [j1_dados.get(c, 0) if isinstance(j1_dados.get(c, 0), (int, float)) else 0 for c in todas_caracteristicas]
            dados_2 = [j2_dados.get(c, 0) if isinstance(j2_dados.get(c, 0), (int, float)) else 0 for c in todas_caracteristicas]

            x = range(len(todas_caracteristicas))

            plt.figure(figsize=(14, 6))
            fig = plt.gcf()
            fig.patch.set_alpha(0.0)

            barras1 = plt.bar(x, dados_1, width=0.4, label=nome1, align='center', color='royalblue', alpha=0.85)
            barras2 = plt.bar([i + 0.4 for i in x], dados_2, width=0.4, label=nome2, align='center', color='green', alpha=0.85)

            for i, valor in enumerate(dados_1):
                plt.text(i, valor + max(dados_1 + dados_2) * 0.02, f'{valor:.2f}', ha='center', fontsize=8, color='white')

            for i, valor in enumerate(dados_2):
                plt.text(i + 0.4, valor + max(dados_1 + dados_2) * 0.02, f'{valor:.2f}', ha='center', fontsize=8, color='white')

            plt.xticks([i + 0.2 for i in x], todas_caracteristicas, rotation=45, ha='right', fontsize=9, color='white')
            plt.yticks(color='white')
            plt.ylabel('Valor', color='white')
            plt.title(f'Comparação: {nome1} vs {nome2}', fontsize=12, color='white')
            plt.grid(axis='y', linestyle='--', alpha=0.3)

            ax = plt.gca()
            for spine in ax.spines.values():
                spine.set_color('white')

            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')

            plt.legend()
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', transparent=True)
            buffer.seek(0)
            imagem_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()

            return imagem_base64

        except Exception as e:
            print(f"Erro ao gerar gráfico: {e}")
            return None
