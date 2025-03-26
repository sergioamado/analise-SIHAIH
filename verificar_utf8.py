import chardet
import os
import codecs

def verificar_e_converter_utf8(caminho_arquivo_entrada, caminho_relatorio_saida):
    """
    Verifica se todas as linhas de um arquivo estão em UTF-8, gera um relatório
    das linhas problemáticas e tenta convertê-las para UTF-8.

    Args:
        caminho_arquivo_entrada (str): O caminho para o arquivo CSV de entrada.
        caminho_relatorio_saida (str): O caminho para o arquivo de relatório TXT.
    """

    linhas_problematicas = []
    total_linhas = 0
    linhas_corrigidas = 0

    try:
        with open(caminho_arquivo_entrada, 'r', encoding='utf-8', errors='ignore') as arquivo:  # Tenta ler como UTF-8, ignora erros iniciais
            for numero_linha, linha in enumerate(arquivo, 1):
                total_linhas += 1
                try:
                    # Tenta decodificar e re-codificar a linha para UTF-8.  Se já estiver OK, não fará nada.
                    linha.encode('utf-8').decode('utf-8')
                except UnicodeDecodeError:
                    linhas_problematicas.append((numero_linha, linha.strip())) # Guarda o número da linha e o conteúdo
                    # Tentativa de conversão usando chardet para detectar a codificação original da linha
                    with open(caminho_arquivo_entrada, 'rb') as f: # Abre novamente em modo binário
                        f.seek(0)  # Garante que o ponteiro esteja no início
                        for i in range(numero_linha):
                            next(f) # Avança para a linha desejada
                        linha_bytes = f.readline() # Lê a linha em bytes

                    result = chardet.detect(linha_bytes)
                    codificacao_detectada = result['encoding']

                    if codificacao_detectada:
                        try:
                            linha_corrigida = linha_bytes.decode(codificacao_detectada, errors='replace').encode('utf-8', errors='replace').decode('utf-8')
                            linhas_corrigidas += 1
                            # Substitui a linha problemática pela corrigida
                            print(f"Linha {numero_linha}: Convertida de {codificacao_detectada} para UTF-8")
                            with codecs.open(caminho_arquivo_entrada, 'r+', encoding='utf-8') as f:
                                linhas = f.readlines()
                                linhas[numero_linha-1] = linha_corrigida + '\n' # Replace na lista
                            with codecs.open(caminho_arquivo_entrada, 'w', encoding='utf-8') as f: # Reescreve o arquivo
                                f.writelines(linhas)
                        except Exception as e:
                            print(f"Erro ao converter linha {numero_linha} de {codificacao_detectada}: {e}")

                    else:
                        print(f"Linha {numero_linha}: Não foi possível detectar a codificação original.")

        # Escrever o relatório
        with open(caminho_relatorio_saida, 'w', encoding='utf-8') as relatorio:
            relatorio.write("Relatório de Linhas Problemáticas (Codificação UTF-8)\n")
            relatorio.write("-" * 50 + "\n")
            relatorio.write(f"Total de linhas processadas: {total_linhas}\n")
            relatorio.write(f"Total de linhas problemáticas encontradas: {len(linhas_problematicas)}\n")
            relatorio.write(f"Total de linhas convertidas com sucesso: {linhas_corrigidas}\n")
            relatorio.write("-" * 50 + "\n")
            for numero_linha, linha in linhas_problematicas:
                relatorio.write(f"Linha {numero_linha}: {linha}\n")

        print(f"Relatório gerado em: {caminho_relatorio_saida}")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {caminho_arquivo_entrada}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


# Exemplo de uso:
caminho_entrada = 'SIHAIH_utf8_convertido.csv'  # Substitua pelo caminho correto
caminho_relatorio = 'relatorio_utf8.txt'

verificar_e_converter_utf8(caminho_entrada, caminho_relatorio)