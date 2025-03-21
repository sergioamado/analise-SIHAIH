import pandas as pd

def converter_para_utf8_com_identificador(input_csv, output_csv="SIHAIH_utf8.csv"):
    """
    Converte um arquivo CSV para codificação UTF-8 e adiciona a coluna 'identificador' no início.

    Args:
        input_csv (str): Caminho para o arquivo CSV de entrada.
        output_csv (str): Caminho para o arquivo CSV de saída com codificação UTF-8.
    """
    try:
        # Ler o arquivo CSV original
        df = pd.read_csv(input_csv, encoding='latin1', low_memory=False)

        # Adicionar a coluna 'identificador' no início
        df.insert(0, 'identificador', range(1, len(df) + 1))  # Adiciona números de 1 até o tamanho do DataFrame

        # Salvar o arquivo com codificação UTF-8
        df.to_csv(output_csv, index=False, encoding='utf-8')

        print(f"Arquivo convertido para UTF-8 e coluna 'identificador' adicionada com sucesso: {output_csv}")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_csv}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# Exemplo de uso
input_csv = "SIHAIH.csv"  # Substitua pelo caminho do seu arquivo CSV
converter_para_utf8_com_identificador(input_csv)