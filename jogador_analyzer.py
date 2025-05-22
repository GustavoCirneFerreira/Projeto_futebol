import chardet
import pandas as pd
import re

class JogadorAnalyzer:
    def __init__(self, arquivos):
        self.dfs = []
        self.dataframes = {}

        for arq in arquivos:
            try:
                posicao = arq.split("/")[-1].replace(".csv", "")
                # Detecta o encoding correto automaticamente
                # Detectar o encoding correto do arquivo
                with open(arq, "rb") as f:
                    encoding_detectado = chardet.detect(f.read())["encoding"]
                df = pd.read_csv(arq, encoding=encoding_detectado, sep=";")

                df.columns = df.columns.str.replace("SalÃ¡rio", "Salário")
                df.columns = df.columns.str.replace("PressÃ£o tentadas", "Pressão tentadas")

                # Adiciona coluna com a posição
                df["Posição"] = posicao

                # Converte valor estimado
                df["Valor Estimado"] = df["Valor Estimado"].apply(self._converter_valor)
                if "Salário" not in df.columns:
                    df["Salário"] = 0
                else:
                    df["Salário"] = df["Salário"].apply(self._converter_salario)

                self.dfs.append(df)
                self.dataframes[posicao] = df  # ESSENCIAL para filtro por posição

            except Exception as e:
                print(f"[ERRO] Falha ao carregar '{arq}': {e}")

        # Junta todos os dataframes, se houver
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
            if mult == "M":
                valor *= 1_000_000
            elif mult == "K":
                valor *= 1_000
            return valor

        return 0.0

    def get_caracteristicas(self):
        colunas_excluidas = [
            "Nome", "Posição", "Valor Estimado", "Clube",
            "Nac", "Pé Preferido", "Idade", "Expira", "Salário"
        ]
        return [col for col in self.df_total.columns if col not in colunas_excluidas and pd.api.types.is_numeric_dtype(self.df_total[col])]

    def get_nomes_jogadores(self):
        return self.df_total["Nome"].dropna().tolist()

    def get_nacionalidades(self):
        if "Nac" in self.df_total.columns:
            return sorted(self.df_total["Nac"].dropna().astype(str).unique().tolist())
        return []

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

    def comparar_jogadores(self, nome1, nome2):
        df = self.df_total
        j1 = df[df["Nome"] == nome1]
        j2 = df[df["Nome"] == nome2]

        if j1.empty or j2.empty:
            return None, None

        return j1.iloc[0], j2.iloc[0]
