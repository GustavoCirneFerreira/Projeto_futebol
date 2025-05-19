import pandas as pd 
import re

class JogadorAnalyzer:
    def __init__(self, arquivos):
        self.dfs = []
        for arq in arquivos:
            posicao = arq.split("/")[-1].replace(".csv", "")
            df = pd.read_csv(arq, encoding="latin1")

            # Adicionar coluna "Posição"
            df["Posição"] = posicao

            # Tratar coluna "Valor Estimado"
            df["Valor Estimado"] = df["Valor Estimado"].apply(self._converter_valor)

            # Tratar altura (ex: "177 cm") → 177
            if "Altura" in df.columns:
                df["Altura"] = df["Altura"].astype(str).str.extract(r"(\d+)").astype(float)

            # Tratar distância percorrida (ex: "458,7 km") → 458.7
            if "Distancia percorrida" in df.columns:
                df["Distancia percorrida"] = (
                    df["Distancia percorrida"]
                    .astype(str)
                    .str.replace(",", ".", regex=False)
                    .str.extract(r"([\d.]+)")
                    .astype(float)
                )

            self.dfs.append(df)

        self.df_total = pd.concat(self.dfs, ignore_index=True)
        self.df_total.fillna(0, inplace=True)

    def _converter_valor(self, valor_str):
        """
        Converte valores do tipo "R$38M - R$115M" ou "Não está à venda" para float
        """
        if not isinstance(valor_str, str):
            return 0

        if "Não está à venda" in valor_str:
            return 0

        # Pegar só o primeiro número
        match = re.search(r"R\$([\d,.]+)([MK]?)", valor_str.replace(".", ""))
        if match:
            valor = float(match.group(1).replace(",", "."))
            multiplicador = match.group(2)
            if multiplicador == "M":
                valor *= 1_000_000
            elif multiplicador == "K":
                valor *= 1_000
            return valor

        return 0

    def get_caracteristicas(self):
        colunas_excluidas = ["Nome", "Posição", "Valor Estimado", "Clube", "Nac", "Pé Preferido", "Idade", "Expira", "Salário"]
        return [col for col in self.df_total.columns if col not in colunas_excluidas and pd.api.types.is_numeric_dtype(self.df_total[col])]

    def get_nomes_jogadores(self):
        return self.df_total["Nome"].dropna().tolist()

    def filtrar_jogadores(self, posicao="Todas", valor_max=None, caracteristicas=[]):
        df_filtrado = self.df_total.copy()

        if posicao != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Posição"] == posicao]

        if valor_max is not None:
            df_filtrado = df_filtrado[df_filtrado["Valor Estimado"] <= valor_max]

        if caracteristicas:
            df_filtrado["Score"] = df_filtrado[caracteristicas].mean(axis=1)
            df_filtrado = df_filtrado.sort_values(by="Score", ascending=False)

        return df_filtrado[["Nome", "Posição", "Valor Estimado"]]

    def comparar_jogadores(self, nome1, nome2):
        df = self.df_total
        j1 = df[df["Nome"] == nome1]
        j2 = df[df["Nome"] == nome2]

        if j1.empty or j2.empty:
            return None, None

        return j1.iloc[0], j2.iloc[0]
