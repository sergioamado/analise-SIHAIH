import pandas as pd
import psycopg2
import logging
import os
from tqdm import tqdm

# Configuração do logging
logging.basicConfig(filename='importacao.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def criar_tabela_e_inserir_dados_postgres(banco_dados, usuario, senha, host, porta, arquivo_csv, batch_size=500):
    """
    Cria a tabela no banco de dados PostgreSQL (se não existir) e insere os dados do CSV em lotes,
    com tratamento de erros e registro em log. Todas as colunas serão do tipo VARCHAR(20).

    Args:
        banco_dados (str): O nome do banco de dados PostgreSQL.
        usuario (str): O nome do usuário do PostgreSQL.
        senha (str): A senha do usuário do PostgreSQL.
        host (str): O endereço do servidor PostgreSQL (e.g., 'localhost').
        porta (int): A porta do servidor PostgreSQL (padrão: 5432).
        arquivo_csv (str): O caminho para o arquivo CSV de entrada.
        batch_size (int): O número de linhas a serem inseridas em cada lote (padrão: 500).
    """

    conexao = None  # Inicializa a variável conexao como None

    try:
        # Conexão com o banco de dados PostgreSQL
        try:
            conexao = psycopg2.connect(database=banco_dados, user=usuario,
                                        password=senha, host=host, port=porta)
            cursor = conexao.cursor()
        except psycopg2.Error as e:
            logging.error(f"Erro ao conectar ao PostgreSQL: {e}")
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            raise  # Re-levanta a exceção para interromper o processo

        # Ler o CSV usando pandas
        try:
            df = pd.read_csv(arquivo_csv, encoding='utf-8', errors='replace', dtype=str) # Força string
        except pd.errors.ParserError as e:
            logging.error(f"Erro ao ler o CSV com Pandas: {e}")
            print(f"Erro ao ler o CSV com Pandas: {e}")
            raise

        # Obter o nome da tabela a partir do nome do arquivo CSV
        nome_tabela = os.path.splitext(os.path.basename(arquivo_csv))[0]
        nome_tabela = ''.join(c for c in nome_tabela if c.isalnum() or c == '_')
        nome_tabela = nome_tabela[:64]
        if not nome_tabela:
            nome_tabela = 'tabela_padrao'

        # Criar a tabela no banco de dados (dinamicamente baseado nas colunas do CSV)
        tipos_colunas = []
        for col in df.columns:
            tipos_colunas.append(f'"{col}" VARCHAR(20)')  # Todas VARCHAR(20)

        # Chave primária
        chave_primaria = '"identificador" INTEGER PRIMARY KEY'

        # Criação da tabela
        sql_criar_tabela = f"""
            CREATE TABLE IF NOT EXISTS "{nome_tabela}" (
                {chave_primaria},
                {', '.join(tipos_colunas)}
            );
        """

        try:
            cursor.execute(sql_criar_tabela)
            conexao.commit()
            print(f"Tabela '{nome_tabela}' criada (ou já existente).")
        except psycopg2.Error as e:
            logging.error(f"Erro ao criar a tabela '{nome_tabela}': {e}")
            print(f"Erro ao criar a tabela '{nome_tabela}': {e}")
            raise

        # Inserir os dados do DataFrame na tabela em lotes
        total_linhas = len(df)
        with tqdm(total=total_linhas, desc=f"Importando para '{nome_tabela}'", unit="linha") as pbar:
            for inicio in range(0, total_linhas, batch_size):
                fim = min(inicio + batch_size, total_linhas)
                batch_df = df[inicio:fim] # Extrai o lote

                try:
                    # Preparar os valores para inserção (converter todos para string e limitar a 20 caracteres)
                    valores = [[str(row[col])[:20] for col in df.columns] for index, row in batch_df.iterrows()]

                    # Criar a string de placeholders para a consulta SQL
                    placeholders = ', '.join(['%s'] * len(df.columns))
                    sql_inserir = f"""
                        INSERT INTO "{nome_tabela}" (
                            {', '.join(f'"{col}"' for col in df.columns)}
                        ) VALUES ({placeholders});
                    """
                    # Executar a consulta SQL com executemany (mais eficiente para múltiplos inserts)
                    cursor.executemany(sql_inserir, valores)
                    conexao.commit()

                    pbar.update(len(batch_df))  # Atualiza a barra de progresso
                except psycopg2.Error as e:
                     logging.error(f"Erro ao inserir lote de linhas {inicio+1}-{fim}: {e}")
                     print(f"Erro ao inserir lote de linhas {inicio+1}-{fim}: {e}")
                     conexao.rollback()

        print("Dados inseridos com sucesso no banco de dados.")

    except FileNotFoundError:
        print(f"Erro: Arquivo CSV não encontrado: {arquivo_csv}")
        logging.error(f"Arquivo CSV não encontrado: {arquivo_csv}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        logging.error(f"Erro inesperado: {e}", exc_info=True)
    finally:
        if conexao:
            cursor.close()
            conexao.close()

# Exemplo de uso:
banco_dados = 'SIHAIH.db'        # Substitua
usuario = 'postegres'          # Substitua
senha = 'cl0ud$'            # Substitua
host = 'localhost'             # Substitua se o banco não for local
porta = 5432                     # Substitua se a porta for diferente da padrão
arquivo_csv = 'SIHAIH_utf8_limpo.csv'

criar_tabela_e_inserir_dados_postgres(banco_dados, usuario, senha, host, porta, arquivo_csv)