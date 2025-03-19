import pandas as pd
import google.generativeai as genai
import os

# Carrega a API Key do arquivo gemini.txt
def load_api_key():
    """Carrega a API Key do arquivo gemini.txt."""
    try:
        with open("api_key_gemini.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Erro: Arquivo api_key_gemini.txt não encontrado. Certifique-se de que ele existe e contém sua API Key.")
        return None

# Inicializa a API do Gemini
api_key = load_api_key()

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        print(f"Erro ao configurar a API Gemini: {e}")
        model = None
else:
    model = None
    
# Carregar o arquivo CSV
try:
    df = pd.read_csv("SIHAIH.csv", encoding='latin1', low_memory=False)  # Tentar com latin1
except FileNotFoundError:
    print("Erro: O arquivo SIHAIH.csv não foi encontrado.")
    exit()
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    try:
        df = pd.read_csv("SIHAIH.csv", encoding='cp1252', low_memory=False) # Tentar com cp1252
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV com cp1252 também: {e}")
        exit()

# Lista de nomes de hospitais desejados
hospitais_desejados = [
    "Hospital de Urgência de Sergipe (HUSE)",
    "Hospital Universitário de Lagarto (HUL-UFS)",
    "Hospital Universitário de Sergipe (HU-UFS)",
    "Hospital Municipal Dr. Nestor Piva",
    "Hospital Cirurgia",
    "Hospital da Criança Dr. José Machado de Souza"
]

def identificar_hospital(cgc_hosp):
    """
    Função para identificar o nome do hospital a partir do CGC_HOSP usando o Gemini.

    Args:
        cgc_hosp (str): O CGC_HOSP do hospital.

    Returns:
        str: O nome do hospital correspondente ou None se não for encontrado.
    """
    if pd.isna(cgc_hosp) or model is None:
        return None

    prompt = f"""
    Você é um sistema especialista em identificar hospitais do estado de Sergipe.
    Dado o seguinte CGC_HOSP: {cgc_hosp}, retorne o nome do hospital correspondente.
    Se não encontrar o hospital, retorne 'Hospital Não Identificado'.
    A saida deve ser somente o nome do hospital ou 'Hospital Não Identificado'.
    """

    try:
        response = model.generate_content(prompt)
        hospital_name = response.text.strip()
        return hospital_name
    except Exception as e:
        print(f"Erro ao consultar o Gemini para CGC_HOSP {cgc_hosp}: {e}")
        return "Erro na Identificação"

# Aplicar a função para identificar o hospital e criar uma nova coluna 'Nome_Hospital'
df['Nome_Hospital'] = '' # Inicializa a coluna para evitar problemas
for index, row in df.iterrows():
    cgc_hosp = str(row['CGC_HOSP'])
    if cgc_hosp != 'nan' and not pd.isna(cgc_hosp):
        df.loc[index, 'Nome_Hospital'] = identificar_hospital(cgc_hosp)
    else:
        df.loc[index, 'Nome_Hospital'] = 'CGC_HOSP Ausente'

# Filtrar o DataFrame para incluir apenas os hospitais desejados
df_filtrado = df[df['Nome_Hospital'].isin(hospitais_desejados)]

# Tratamento de dados ausentes (substituindo NA por 'Não Informado')
df_filtrado = df_filtrado.fillna('Não Informado')

# Remover colunas desnecessárias (opcional, ajuste conforme necessário)
colunas_para_remover = ['Unnamed: 0']  # Remova a coluna de índice se existir
df_filtrado = df_filtrado.drop(columns=colunas_para_remover, errors='ignore')

# Salvar o DataFrame filtrado e tratado em um novo arquivo CSV
try:
    df_filtrado.to_csv("SIHAIH_hospitais_selecionados.csv", index=False, encoding='utf-8')
    print("Arquivo SIHAIH_hospitais_selecionados.csv gerado com sucesso.")
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV: {e}")