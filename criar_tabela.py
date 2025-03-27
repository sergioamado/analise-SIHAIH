import pandas as pd
import subprocess

csv_path = "SIHAIH_utf8.csv" 
df = pd.read_csv(csv_path)

tipos_sql = []
colunas_tabela = []

for coluna in df.columns:
    coluna_tabela = "sem_nome" if "Unnamed" in coluna else coluna  # Renomeia colunas sem nome
    colunas_tabela.append(coluna_tabela)

df.columns = colunas_tabela

for coluna in df.columns:
    if df[coluna].dtype == "int64":
        tipos_sql.append(f"{coluna} BIGINT")
    elif df[coluna].dtype == "float64":
        tipos_sql.append(f"{coluna} DECIMAL")
    else:
        tipos_sql.append(f"{coluna} TEXT")
    
nome_tabela = "dados_sihaih"
create_table_sql = f"CREATE TABLE {nome_tabela} (\n    " + ",\n    ".join(tipos_sql) + "\n);"

with open("dados_sihaih.sql", "w") as f:
    f.write(create_table_sql)

print("Arquivo dados_sihaih.sql gerado com sucesso!")


DATABASE_NAME = "sihaih"
sql_path = "./dados_sihaih.sql"
run_table = f'psql -U postgres -d {DATABASE_NAME} -f {sql_path}'

subprocess.run(run_table, shell=True)

print("Tabela criada com sucesso no banco de dados")