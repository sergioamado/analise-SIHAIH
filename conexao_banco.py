import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import chardet

def criar_banco_e_tabela(db_name, user, password, host, port, csv_file):
    """
    Cria um banco de dados PostgreSQL, uma tabela e importa os dados de um CSV.

    Args:
        db_name (str): Nome do banco de dados.
        user (str): Nome do usuário do PostgreSQL.
        password (str): Senha do usuário do PostgreSQL.
        host (str): Host do servidor PostgreSQL.
        port (str): Porta do servidor PostgreSQL.
        csv_file (str): Caminho para o arquivo CSV.
    """
    try:
        # Detectar a codificação do arquivo CSV
        with open(csv_file, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']
        print(f"Codificação detectada: {encoding}")

        # Tentar conectar ao PostgreSQL (sem especificar o banco de dados)
        conn = psycopg2.connect(user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cursor = conn.cursor()

        # Criar o banco de dados se ele não existir
        cursor.execute(f"CREATE DATABASE {db_name};")
        print(f"Banco de dados '{db_name}' criado com sucesso.")

        # Conectar ao banco de dados recém-criado
        conn.close()
        conn = psycopg2.connect(database=db_name, user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cursor = conn.cursor()

        # Ler o CSV usando Pandas com a codificação detectada
        df = pd.read_csv(csv_file, encoding=encoding, low_memory=False)

        # Imprimir informações sobre os tipos de dados
        print("\nTipos de dados detectados pelo Pandas:")
        print(df.dtypes)

        # Criar a tabela no PostgreSQL
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

        # Inferir tipos de dados do Pandas para o PostgreSQL
        def tipo_pandas_para_postgres(tipo_pandas):
            if tipo_pandas == 'int64':
                return 'INTEGER'
            elif tipo_pandas == 'float64':
                return 'NUMERIC'
            elif tipo_pandas == 'datetime64[ns]':
                return 'TIMESTAMP'
            else:
                return 'VARCHAR(255)'  # Default para strings

        # Cria a string com os tipos de dados para a criação da tabela
        colunas_sql = ",\n".join([f'    "{col}" {tipo_pandas_para_postgres(str(df[col].dtype))}' if col != 'identificador' else '    identificador INTEGER PRIMARY KEY' for col in df.columns])

        # Comando SQL para criar a tabela
        create_table_sql = f"""
            CREATE TABLE dados_unificados (
                {colunas_sql}
            );
        """

        # Executar o comando para criar a tabela
        cursor.execute(create_table_sql)
        print("Tabela 'dados_unificados' criada com sucesso.")

        # Importar dados do CSV para a tabela usando to_sql
        df.to_sql('dados_unificados', engine, if_exists='append', index=False)
        print("Dados importados para a tabela 'dados_unificados' com sucesso.")

    except psycopg2.Error as e:
        print(f"Erro de PostgreSQL: {e}")
    except FileNotFoundError:
        print("Arquivo CSV não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        if conn:
            conn.close()

# Dados de conexão (substitua com suas credenciais)
db_name = "SIHAIH"
user = "postgres"  # Usuário padrão do PostgreSQL
password = "cl0ud$"  # Sua senha
host = "localhost"
port = "5432"  # Porta padrão do PostgreSQL

# Arquivo CSV
csv_file = "SIHAIH.csv"

# Criar o banco de dados e a tabela
criar_banco_e_tabela(db_name, user, password, host, port, csv_file)