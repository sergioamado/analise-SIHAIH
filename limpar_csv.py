import pandas as pd
import chardet

def limpar_e_contar_na(input_csv, output_csv, relatorio_txt):
    """
    Limpa um arquivo CSV, removendo aspas duplas de colunas numéricas e NAs,
    e gera um relatório da remoção com indicador de progresso.

    Args:
        input_csv (str): Caminho para o arquivo CSV de entrada.
        output_csv (str): Caminho para o arquivo CSV de saída (limpo).
        relatorio_txt (str): Caminho para o arquivo de texto de relatório.
    """

    try:
        # Ler o CSV (detectar a codificação primeiro)
        with open(input_csv, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

        print(f"Codificação detectada: {encoding}") # Adicionado para verificar a codificação

        df = pd.read_csv(input_csv, encoding=encoding, low_memory=False)

        # Inicializar contadores
        total_na_removidos = 0
        contagem_por_coluna = {}

        # Identificar colunas numéricas
        colunas_numericas = df.select_dtypes(include=['number']).columns
        num_colunas_numericas = len(colunas_numericas) # Para evitar recalculos

        # Limpar aspas duplas das colunas numéricas
        for i, coluna in enumerate(colunas_numericas):
            df[coluna] = df[coluna].astype(str).str.replace('"', '', regex=False).astype(float, errors='ignore')  # Remove aspas e converte para float
            progresso = (i + 1) / num_colunas_numericas * 100
            print(f"Limpeza das colunas numéricas: {progresso:.2f}% concluído", end='\r')

        print() # Quebra de linha após a conclusão

        # Substituir "NA" por NaN
        df.replace('NA', pd.NA, inplace=True)

        # Contar e remover NaN
        total_colunas = len(df.columns)
        for i, coluna in enumerate(df.columns):
            contagem_na = df[coluna].isna().sum()
            if contagem_na > 0:
                #Imprime quais colunas possuem valores nulos para ver se o processo está funcionando
                print(f"A coluna {coluna} possui {contagem_na} valores nulos")
                #Antes estava usando o dropna, o que removia linhas do csv.
                #Agora iremos percorrer os valores nulos e substituir por vazio
                df[coluna] = df[coluna].fillna('')

                contagem_por_coluna[coluna] = contagem_na
                total_na_removidos += contagem_na
            progresso = (i + 1) / total_colunas * 100
            print(f"Processando colunas: {progresso:.2f}% concluído", end='\r')

        print() # Quebra de linha após a conclusão

        # Gerar relatório
        with open(relatorio_txt, 'w') as f:
            f.write("Relatório de Remoção de NAs\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total de NAs removidos: {total_na_removidos}\n\n")
            f.write("Contagem por coluna:\n")
            for coluna, contagem in contagem_por_coluna.items():
                f.write(f"- {coluna}: {contagem}\n")

        # Salvar o CSV limpo
        df.to_csv(output_csv, encoding='utf-8', index=False)
        print(f"Arquivo limpo e salvo como: {output_csv}")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_csv}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

import chardet

# Exemplo de uso
input_file = "SIHAIH.csv"  # Substitua pelo nome do seu arquivo CSV
output_file = "SIHAIH_limpo.csv"  # Nome do arquivo CSV de saída
relatorio_file = "relatorio_na.txt"  # Nome do arquivo de relatório

limpar_e_contar_na(input_file, output_file, relatorio_file)