import pandas as pd

def combinar_csv(partes_csv, output_file="resultado_combinado.csv"):
    """
    Combina múltiplos arquivos CSV em um único arquivo, mantendo a coluna 'identificador' apenas uma vez.

    Args:
        partes_csv (list): Lista de caminhos para os arquivos CSV a serem combinados.
        output_file (str): Nome do arquivo CSV resultante.
    """
    try:
        # 1. Ler os arquivos CSV
        dataframes = [pd.read_csv(parte, encoding='latin1', low_memory=False) for parte in partes_csv]

        # 2. Combinar os DataFrames horizontalmente com base na coluna 'identificador'
        df_combinado = dataframes[0]
        for df in dataframes[1:]:
            df_combinado = pd.merge(df_combinado, df, on="identificador", how="inner")

        # 3. Salvar o DataFrame combinado em um único arquivo CSV
        df_combinado.to_csv(output_file, index=False, encoding='utf-8')

        print(f"Arquivos combinados com sucesso em '{output_file}'.")

    except FileNotFoundError as e:
        print(f"Erro: Um dos arquivos CSV não foi encontrado. {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# Lista de arquivos CSV gerados
partes_csv = ["parte1.csv", "parte2.csv", "parte3.csv"]

# Nome do arquivo resultante
output_file = "resultado_combinado.csv"

# Combinar os arquivos CSV
combinar_csv(partes_csv, output_file)