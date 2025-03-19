import pandas as pd

def dividir_csv(input_csv, output_prefix="parte"):
    """
    Divide um arquivo CSV em três partes com uma coluna de identificador.

    Args:
        input_csv (str): Caminho para o arquivo CSV de entrada.
        output_prefix (str): Prefixo para os nomes dos arquivos de saída (ex: "parte").
    """
    try:
        # Ler o CSV
        df = pd.read_csv(input_csv, encoding='latin1', low_memory=False)

        # 1. Criar a coluna 'identificador'
        df['identificador'] = range(1, len(df) + 1)  # Números de 1 até o tamanho do DataFrame

        # 2. Dividir as colunas em três partes (aproximadamente iguais)
        colunas = df.columns.tolist()
        colunas.remove('identificador')  # Remover 'identificador' para dividir as outras colunas

        num_colunas = len(colunas)
        tamanho_parte = num_colunas // 3

        parte1_colunas = ['identificador'] + colunas[:tamanho_parte]
        parte2_colunas = ['identificador'] + colunas[tamanho_parte:2 * tamanho_parte]
        parte3_colunas = ['identificador'] + colunas[2 * tamanho_parte:]

        df_parte1 = df[parte1_colunas]
        df_parte2 = df[parte2_colunas]
        df_parte3 = df[parte3_colunas]

        # 3. Salvar cada parte em um arquivo CSV
        df_parte1.to_csv(f"{output_prefix}1.csv", encoding='utf-8', index=False)
        df_parte2.to_csv(f"{output_prefix}2.csv", encoding='utf-8', index=False)
        df_parte3.to_csv(f"{output_prefix}3.csv", encoding='utf-8', index=False)

        print("Arquivo CSV dividido em três partes com sucesso.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_csv}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# Exemplo de uso
input_file = "SIHAIH.csv"  # Substitua pelo nome do seu arquivo CSV
dividir_csv(input_file)  # Divide o arquivo