import streamlit as st
import pandas as pd
import plotly.express as px
import io
import numpy as np  # Importe o NumPy

# Funções para análise de qualidade de dados
def identificar_ruido_idade(df):
    """Identifica ruído na coluna IDADE (valores negativos ou > 120)."""
    try:
        # Verifique se a coluna 'IDADE' existe
        if 'IDADE' not in df.columns:
            st.error("Coluna 'IDADE' não encontrada no DataFrame.")
            return pd.DataFrame()

        # Converta a coluna para numérico e force valores não numéricos a NaN
        df['IDADE'] = pd.to_numeric(df['IDADE'], errors='coerce')

        # Remova valores NaN da coluna 'IDADE' para evitar erros futuros
        df_sem_nan = df.dropna(subset=['IDADE'])

        # Identifique o ruído
        ruido = df_sem_nan[((df_sem_nan['IDADE'] < 0) | (df_sem_nan['IDADE'] > 120))]

        return ruido

    except Exception as e:
        st.error(f"Erro ao analisar ruído na coluna IDADE: {e}")
        return pd.DataFrame()

def identificar_outliers_diarias(df):
    """Identifica outliers na coluna QT_DIARIAS (valores > 365)."""
    try:
        # Verifique se a coluna 'QT_DIARIAS' existe
        if 'QT_DIARIAS' not in df.columns:
            st.error("Coluna 'QT_DIARIAS' não encontrada no DataFrame.")
            return pd.DataFrame()

        # Converta a coluna para numérico e force valores não numéricos a NaN
        df['QT_DIARIAS'] = pd.to_numeric(df['QT_DIARIAS'], errors='coerce')

        # Remova valores NaN da coluna 'QT_DIARIAS' para evitar erros futuros
        df_sem_nan = df.dropna(subset=['QT_DIARIAS'])

        # Identifique outliers
        outliers = df_sem_nan[df_sem_nan['QT_DIARIAS'] > 365]

        return outliers

    except Exception as e:
        st.error(f"Erro ao analisar outliers na coluna QT_DIARIAS: {e}")
        return pd.DataFrame()

def calcular_incompletude(df, coluna):
    """Calcula a porcentagem de valores ausentes em uma coluna."""
    try:
        # Verifique se a coluna existe
        if coluna not in df.columns:
            st.error(f"Coluna '{coluna}' não encontrada no DataFrame.")
            return 0.0  # Retorna 0 para evitar erros futuros

        # Calcule o total de linhas e valores ausentes
        total = len(df)
        ausentes = df[coluna].isnull().sum()

        # Calcule a porcentagem de valores ausentes
        porcentagem = (ausentes / total) * 100 if total > 0 else 0.0

        return porcentagem

    except Exception as e:
        st.error(f"Erro ao calcular incompletude na coluna {coluna}: {e}")
        return 0.0  # Retorna 0 para evitar erros futuros

def identificar_inconsistencia_datas(df):
    """Identifica inconsistências entre DT_SAIDA e DT_INTER."""
    try:
        # Verifique se as colunas de data existem
        if 'DT_SAIDA' not in df.columns or 'DT_INTER' not in df.columns:
            st.error("Colunas de data (DT_SAIDA ou DT_INTER) não encontradas no DataFrame.")
            return pd.DataFrame()

        # Converta as colunas para datetime e force valores inválidos a NaT
        df['DT_SAIDA'] = pd.to_datetime(df['DT_SAIDA'], errors='coerce')
        df['DT_INTER'] = pd.to_datetime(df['DT_INTER'], errors='coerce')

        # Remova linhas com valores NaN nas colunas de data para evitar erros futuros
        df_sem_nan = df.dropna(subset=['DT_SAIDA', 'DT_INTER'])

        # Identifique inconsistências
        inconsistencias = df_sem_nan[df_sem_nan['DT_SAIDA'] < df_sem_nan['DT_INTER']]

        return inconsistencias

    except Exception as e:
        st.error(f"Erro ao analisar inconsistência entre datas: {e}")
        return pd.DataFrame()

def contar_dados_invalidos(df):
    """Conta dados em branco/fora do tipo em cada coluna."""
    contagem = {}
    for col in df.columns:
        # Dados em branco (NaN)
        nulos = df[col].isnull().sum()
        contagem[f'Nulos em {col}'] = nulos

        # Dados fora do tipo
        if df[col].dtype == 'object':
            continue  # Ignora colunas de texto
        try:
            #Tentar converter para numérico
            df[col] = pd.to_numeric(df[col], errors='coerce')  #trata erros
            #Dados inválidos seriam aqueles que não conseguiram ser convertidos
            nao_numericos = df[col].isnull().sum()
            contagem[f'Dados inválidos em {col}'] = nao_numericos - nulos

        except ValueError:
            contagem[f'Dados inválidos em {col}'] = len(df) - nulos

    return contagem

def calcular_quantidade_dados(df, hospital):
    """Calcula a quantidade de dados para um hospital específico."""
    try:
        # Verifique se a coluna 'CGC_HOSP' existe
        if 'CGC_HOSP' not in df.columns:
            st.error("Coluna 'CGC_HOSP' não encontrada no DataFrame.")
            return 0

        # Calcule a quantidade de dados para o hospital
        quantidade = len(df[df['CGC_HOSP'] == hospital])

        return quantidade

    except Exception as e:
        st.error(f"Erro ao calcular quantidade de dados para o hospital: {e}")
        return 0

def limpar_dados(df):
    """Remove aspas extras e converte valores NA para NaN."""
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                # Primeiro, remove aspas extras
                df[col] = df[col].str.replace('"', '')
                # Agora, tenta converter valores NA para NaN
                df[col] = df[col].replace('NA', pd.NA)
            except:
                pass
    return df

def load_csv(filename="hfiltrado.csv"):
    """Carrega o arquivo CSV do SIHAIH."""
    try:
        df = pd.read_csv(filename, encoding='utf-8')
        return df
    except FileNotFoundError:
        st.error(f"Arquivo {filename} não encontrado. Certifique-se de que ele existe e está no mesmo diretório do script.")
        return None
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filename, encoding='latin1')  # Tenta outra codificação
            return df
        except Exception as e:
            st.error(f"Erro ao ler o arquivo {filename}: {e}")
            return None
    except Exception as e:
        st.error(f"Erro ao ler o arquivo {filename}: {e}")
        return None

# Interface Streamlit
st.title("Análise de Qualidade de Dados SIHAIH (hfiltrado.csv)")

# Carrega o DataFrame do SIHAIH.csv
df = load_csv()

if df is not None:

    # Limpa aspas e NAs
    df = limpar_dados(df)

    # Dropa a coluna "Unnamed: 0" se existir
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Exibe o DataFrame
    st.write("Pré-visualização dos Dados:")
    st.dataframe(df.head())

    # Análise de Qualidade de Dados
    st.header("Análise de Qualidade de Dados (hfiltrado.csv)")

    # Ruído na coluna IDADE
    st.subheader("Ruído na Coluna IDADE")
    ruido_idade = identificar_ruido_idade(df)
    if not ruido_idade.empty:
        st.warning(f"Foram encontrados {len(ruido_idade)} registros com ruído na coluna IDADE.")
        st.dataframe(ruido_idade)
    else:
        st.success("Nenhum ruído encontrado na coluna IDADE.")

    # Outliers na coluna QT_DIARIAS
    st.subheader("Outliers na Coluna QT_DIARIAS")
    outliers_diarias = identificar_outliers_diarias(df)
    if not outliers_diarias.empty:
        st.warning(f"Foram encontrados {len(outliers_diarias)} outliers na coluna QT_DIARIAS.")
        st.dataframe(outliers_diarias)
    else:
        st.success("Nenhum outlier encontrado na coluna QT_DIARIAS.")

    # Incompletude na coluna DIAG_SECUN
    st.subheader("Incompletude na Coluna DIAG_SECUN")
    porcentagem_ausente = calcular_incompletude(df, 'DIAG_SECUN')
    st.info(f"A coluna DIAG_SECUN tem {porcentagem_ausente:.2f}% de valores ausentes.")
    if porcentagem_ausente > 50:  # Exemplo de limite
        st.warning("A coluna DIAG_SECUN tem uma alta porcentagem de valores ausentes. Considere não utilizá-la na análise.")

    # Inconsistência entre DT_SAIDA e DT_INTER
    st.subheader("Inconsistência entre DT_SAIDA e DT_INTER")
    inconsistencia_datas = identificar_inconsistencia_datas(df)

    if not inconsistencia_datas.empty:
        st.warning(f"Foram encontrados {len(inconsistencia_datas)} registros com DT_SAIDA anterior a DT_INTER.")
        st.dataframe(inconsistencia_datas)
    else:
        st.success("Nenhuma inconsistência encontrada entre DT_SAIDA e DT_INTER.")

   # Contagem de dados inválidos e gráficos
    st.subheader("Dados Inválidos (Nulos e Fora do Tipo)")
    contagem_invalidos = contar_dados_invalidos(df)
    st.write(contagem_invalidos)  # Exibe a contagem

    # Gráfico de barras para dados inválidos
    df_contagem = pd.DataFrame.from_dict(contagem_invalidos, orient='index', columns=['Contagem'])
    fig_invalidos = px.bar(df_contagem, x=df_contagem.index, y='Contagem', title='Contagem de Dados Inválidos por Coluna')
    st.plotly_chart(fig_invalidos)

    #Contar quantidade de dados em cada hospital
    st.subheader("Quantidade de Dados por Hospital")
    hospitais_contagem = {}
    hospitais= [
        "Hospital de Urgência de Sergipe (HUSE)",
        "Hospital Universitário de Lagarto (HUL-UFS)",
        "Hospital Universitário de Sergipe (HU-UFS)",
        "Hospital Municipal Dr. Nestor Piva",
        "Hospital Cirurgia",
        "Hospital da Criança Dr. José Machado de Souza"
    ]


    for hospital in hospitais:
        quantidade = calcular_quantidade_dados(df, hospital)
        st.write(f"Quantidade de dados para {hospital}: {quantidade}")
        if quantidade < 100:  # Exemplo de limite
            st.warning(f"A quantidade de dados para {hospital} é baixa ({quantidade}). As conclusões podem ser limitadas.")
        hospitais_contagem[hospital] = quantidade
    # Grafico de quantidade por hospital
    df_hospitais = pd.DataFrame.from_dict(hospitais_contagem, orient='index', columns=['Contagem'])
    fig_hospitais = px.bar(df_hospitais, x=df_hospitais.index, y='Contagem', title='Contagem de Dados por Hospital')
    st.plotly_chart(fig_hospitais)



    # Verificar Pontualidade dos Dados
    st.subheader("Pontualidade dos Dados")
    try:
        anos = df['ANO_CMPT'].unique()  # Supondo que 'ANO_CMPT' indica o ano dos dados
        st.write(f"Anos presentes nos dados: {anos}")
        ano_mais_antigo = min(anos)
        if ano_mais_antigo < 2010:
            st.warning("Os dados contêm informações de anos anteriores a 2010. Considere se esses dados antigos ainda são relevantes para sua análise.")
    except KeyError:
        st.error("Coluna 'ANO_CMPT' não encontrada no DataFrame.")
    except Exception as e:
        st.error(f"Erro ao verificar a pontualidade dos dados: {e}")


    # Gerar Relatório
    st.header("Relatório de Análise de Qualidade de Dados")
    st.write("Um relatório resumido das principais descobertas será gerado aqui.")
    # Aqui você pode adicionar um código para gerar um relatório mais detalhado
    # com as descobertas, como número de ruídos, outliers, dados faltantes, etc.

    st.header("Resumo do Artigo")
    resumo_artigo_text = """
    ## Resumo do Artigo "Uma Taxonomia dos Desafios de Qualidade de Dados em Engenharia de Software Empírica"

    O artigo de Bosu e MacDonell (2013) apresenta uma taxonomia de desafios de qualidade de dados no contexto da Engenharia de Software Empírica (ESE). O objetivo principal é aumentar a conscientização sobre os problemas que podem afetar a qualidade dos dados utilizados na modelagem em ESE, visando melhorar tanto a pesquisa quanto a prática na área.

    ### Principais Pontos:

    1.  **Motivação:** A qualidade dos dados é crucial para a confiabilidade de modelos empíricos utilizados em ESE, como os de estimativa de esforço e predição de defeitos. Dados de baixa qualidade podem levar a modelos imprecisos e decisões erradas.

    2.  **Taxonomia:** A taxonomia proposta divide os problemas de qualidade de dados em três classes principais:
        *   **Precisão:** Características dos dados que indicam que eles não são adequados para modelagem (ruído, outliers, incompletude, inconsistência, redundância).
        *   **Relevância:** Características dos conjuntos de dados que levantam preocupações sobre a aplicabilidade de um modelo a outro conjunto de dados (heterogeneidade, quantidade de dados, pontualidade).
        *   **Proveniência:** Fatores que impedem ou limitam a acessibilidade e a confiança nos dados (sensibilidade comercial, acessibilidade, confiabilidade).

    3.  **Discussão:** A revisão da literatura revelou que as questões de precisão são as mais abordadas na pesquisa em ESE, enquanto as de proveniência recebem menos atenção.

    4.  **Conclusões:** A proveniência dos dados é um aspecto subexplorado em ESE, e investir em sistemas de proveniência pode melhorar a qualidade dos dados e dos modelos derivados. A colaboração entre academia e indústria é essencial para entender e melhorar a gestão da qualidade dos dados na prática.

    ### Como o artigo pode te ajudar no seu CSV do SIHAIH:

    O artigo pode te ajudar a entender e mitigar problemas de qualidade de dados no seu CSV do SIHAIH. Aqui estão algumas aplicações práticas:

    #### 1. Identificação de Problemas de Qualidade:

        *   **Precisão:**
            *   **Ruído:** Verificar se há valores obviamente errados ou impossíveis em alguma coluna (ex: idade negativa, datas inválidas).
            *   **Outliers:** Identificar valores extremos em colunas como `QT_DIARIAS`, `VAL_TOT`, `IDADE` que podem indicar erros de digitação ou casos atípicos que merecem investigação.
            *   **Incompletude:** Analisar a quantidade de valores ausentes em cada coluna e decidir como lidar com eles (ex: imputação, remoção de linhas). Colunas com muitos valores ausentes podem não ser úteis para análise.
            *   **Inconsistência:** Verificar se há valores inconsistentes entre colunas (ex: data de saída anterior à data de internação, sexo incompatível com o código do procedimento).

        *   **Relevância:**

            *   **Heterogeneidade:** Se você tiver dados de diferentes hospitais, considerar se há diferenças significativas nas práticas de registro de dados que podem afetar a comparação entre eles.
            *   **Quantidade de Dados:** Avaliar se o número de registros para cada hospital é suficiente para realizar análises estatísticas significativas.
            *   **Pontualidade:** Considerar se os dados são recentes o suficiente para refletir as práticas atuais. Se os dados forem muito antigos, eles podem não ser relevantes para o seu objetivo.

        *   **Proveniência:**

            *   **Acessibilidade:** Entender como os dados foram coletados e quem foi responsável pela coleta. Isso pode te ajudar a avaliar a confiabilidade dos dados.
            *   **Confiabilidade:** Avaliar a qualidade dos processos de coleta e verificação de dados nos hospitais. Isso pode te dar uma ideia do quão confiáveis são os dados.

    #### 2. Pré-Processamento de Dados:

        *   O artigo discute técnicas para lidar com ruído, outliers e valores ausentes. Você pode aplicar essas técnicas para limpar seus dados antes de realizar análises.

    #### 3. Interpretação dos Resultados:

        *   Estar ciente dos problemas de qualidade de dados pode te ajudar a interpretar os resultados das suas análises com mais cautela.

        *   Considerar como os problemas de qualidade de dados podem ter afetado os resultados e comunicar essas limitações.
    """
    st.markdown(resumo_artigo_text)

else:
    st.info("Certifique-se de que o arquivo 'hfiltrado.csv' está no mesmo diretório do script e que ele foi gerado pelo script de filtro com Gemini.")