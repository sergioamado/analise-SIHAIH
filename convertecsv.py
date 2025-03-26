import pandas as pd
import chardet

def converter_e_verificar_utf8(caminho_arquivo_entrada, caminho_arquivo_saida):
    """
    Converte um arquivo CSV codificado em SIHAIH (possivelmente uma variação de ANSI) para UTF-8,
    verifica se a conversão foi bem-sucedida e salva o resultado.

    Args:
        caminho_arquivo_entrada (str): O caminho para o arquivo CSV de entrada (SIHAIH_utf8.csv).
        caminho_arquivo_saida (str): O caminho para o arquivo CSV de saída (em UTF-8).
    """

    try:
        # 1. Detectar a codificação original (mais robusto)
        with open(caminho_arquivo_entrada, 'rb') as f:
            result = chardet.detect(f.read())
            codificacao_original = result['encoding']
        print(f"Codificação detectada: {codificacao_original}")

        if codificacao_original is None:
            print("Erro: Não foi possível detectar a codificação do arquivo.  Tente especificar a codificação manualmente (e.g., 'latin1', 'cp1252').")
            return False  # Falha na detecção

        # 2. Ler o CSV usando pandas, especificando a codificação detectada
        df = pd.read_csv(caminho_arquivo_entrada, encoding=codificacao_original)

        # 3. Salvar o CSV em UTF-8
        df.to_csv(caminho_arquivo_saida, encoding='utf-8', index=False) # index=False para não salvar o índice

        # 4. Verificar a conversão (amostra) - leia algumas linhas do arquivo UTF-8
        try:
            with open(caminho_arquivo_saida, 'r', encoding='utf-8') as f:
                primeiras_linhas = [next(f) for _ in range(5)] # Ler as 5 primeiras linhas
            print("\nPrimeiras linhas do arquivo convertido (UTF-8):\n", "".join(primeiras_linhas))

            # Tenta decodificar as linhas para garantir que UTF-8 está funcionando
            for linha in primeiras_linhas:
                linha.encode('utf-8').decode('utf-8') # Teste básico de decodificação
            print("A conversão para UTF-8 parece bem-sucedida (teste de decodificação OK).")
            return True  # Conversão bem-sucedida

        except UnicodeDecodeError as e:
            print(f"Erro ao verificar o arquivo UTF-8: Problema de decodificação.  A conversão pode não ter sido totalmente bem-sucedida.\nErro: {e}")
            return False # Falha na verificação

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {caminho_arquivo_entrada}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False

# Exemplo de uso:
caminho_entrada = 'SIHAIH_utf8.csv'
caminho_saida = 'SIHAIH_utf8_convertido.csv'

if converter_e_verificar_utf8(caminho_entrada, caminho_saida):
    print(f"Arquivo convertido e salvo como: {caminho_saida}")
else:
    print("A conversão falhou. Verifique as mensagens de erro.")