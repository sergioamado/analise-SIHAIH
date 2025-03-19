import pandas as pd

def converter_para_utf8(input_csv, output_csv):
    """
    Converte um arquivo CSV para UTF-8 e lida com erros de decodificação.

    Args:
        input_csv (str): Caminho para o arquivo CSV de entrada.
        output_csv (str): Caminho para o arquivo CSV de saída (UTF-8).
    """
    try:
        # Tenta ler o CSV com diferentes codificações
        for encoding in ['latin1', 'cp1252', 'utf-8']:
            try:
                df = pd.read_csv(input_csv, encoding=encoding, low_memory=False)
                print(f"Arquivo lido com sucesso usando a codificação: {encoding}")
                break  # Se a leitura for bem-sucedida, interrompe o loop
            except UnicodeDecodeError:
                print(f"Falha ao ler com a codificação: {encoding}")
        else:
            print("Falha ao ler o arquivo com as codificações testadas.")
            return False # Falha na conversão

        # Tratar valores ausentes (NaN) - Opcional, remova se não precisar
        df = df.fillna('') # Substitui NaN por string vazia

        # Salvar o DataFrame como CSV em UTF-8
        df.to_csv(output_csv, encoding='utf-8', index=False)
        print(f"Arquivo convertido para UTF-8 e salvo como: {output_csv}")
        return True # Conversão bem sucedida

    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_csv}' não foi encontrado.")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False


# Exemplo de uso
input_csv_file = "SIHAIH_hospitais_selecionados.csv" # Substitua pelo nome do seu arquivo de entrada
output_csv_file = "SIHAIH_hospitais_selecionados_utf8.csv" # Substitua pelo nome desejado do arquivo de saída

if converter_para_utf8(input_csv_file, output_csv_file):
    print("Conversão concluída com sucesso!")
else:
    print("A conversão falhou.")