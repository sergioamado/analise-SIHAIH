import codecs
import unicodedata

def limpar_e_converter_utf8(caminho_arquivo_entrada, caminho_arquivo_saida):
    """
    Limpa caracteres não imprimíveis e converte para UTF-8.
    """
    try:
        with codecs.open(caminho_arquivo_entrada, 'r', encoding='utf-8', errors='replace') as entrada:
            with codecs.open(caminho_arquivo_saida, 'w', encoding='utf-8') as saida:
                for linha in entrada:
                    # Remove caracteres de controle e não imprimíveis
                    linha_limpa = ''.join(c for c in linha if unicodedata.category(c)[0] != 'C')
                    saida.write(linha_limpa)
        print(f"Arquivo limpo e convertido salvo como: {caminho_arquivo_saida}")
        return True
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return False
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False

caminho_entrada = 'SIHAIH_utf8_convertido.csv'
caminho_saida = 'SIHAIH_utf8_limpo.csv'
if limpar_e_converter_utf8(caminho_entrada, caminho_saida):
    arquivo_csv = caminho_saida # Atualiza o nome do arquivo
else:
    print("Falha na limpeza e conversão.")