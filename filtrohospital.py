import pandas as pd

# Lista de CNES dos hospitais desejados
cnes_hospitais = [
    '2816210',  # Hospital de Urgência de Sergipe (HUSE)
    '7903081',  # HOSPITAL UNIV MONSENHOR JOAO BATISTA DE CARVALHO DALTRO (HUL)
    '6568343',  # HOSPITAL UNIV MONSENHOR JOAO BATISTA DE CARVALHO DALTRO (Duplicado, manter apenas um se for o caso)
    '0002534',  # HOSPITAL UNIVERSITARIO DE SERGIPE
    '3841375',  # HOSPITAL MUNICIPAL ZONA NORTE DR NESTOR PIVA
    '0002283',  # HOSPITAL DE CIRURGIA
    '2477955'   # HOSPITAL DA CRIANCA DR JOSE MACHADO DE SOUZA
]

# Arquivo AH_CNES original (substitua pelo caminho real do seu arquivo)
arquivo_ah_cnes = 'SIHAIH_utf8.csv'  # Ajuste o nome/caminho se necessário.

# Arquivo CSV de saída
arquivo_saida = 'hospitais_sergipe.csv'

def filtrar_e_salvar_hospitais(arquivo_entrada, lista_cnes, arquivo_saida):
    """
    Filtra os dados do arquivo AH_CNES para os hospitais especificados
    e salva em um novo arquivo CSV.

    Args:
        arquivo_entrada (str): Caminho para o arquivo AH_CNES.
        lista_cnes (list): Lista dos CNES dos hospitais a serem filtrados.
        arquivo_saida (str): Caminho para o arquivo CSV de saída.
    """
    try:
        # Carrega o arquivo AH_CNES (detecta automaticamente a codificação)
        df = pd.read_csv(arquivo_entrada, encoding='utf-8', low_memory=False)
        # Filtra os dados pelo CNES
        df_filtrado = df[df['CNES'].isin(lista_cnes)]

        # Salva o DataFrame filtrado em um novo arquivo CSV
        df_filtrado.to_csv(arquivo_saida, index=False, encoding='utf-8')

        print(f"Dados filtrados e salvos em: {arquivo_saida}")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {arquivo_entrada}")
    except KeyError:
        print("Erro: A coluna 'CNES' não foi encontrada no arquivo.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


# Chama a função para filtrar e salvar os dados
filtrar_e_salvar_hospitais(arquivo_ah_cnes, cnes_hospitais, arquivo_saida)

print("Processo concluído.")