from io import StringIO
import pandas as pd
import subprocess

csv_path = "SIHAIH_utf8.csv"
df = pd.read_csv(csv_path, low_memory=False)

colunas = [col for col in df.columns if col != "Unnamed: 0"]

csv_buffer = StringIO()
df[colunas].to_csv(csv_buffer, index=False, header=True)
csv_buffer.seek(0)

database_name = "sihaih"
table_name = "dados_sihaih"
colunas_sql = ", ".join(colunas)  

copy_cmd = f"\COPY {table_name} ({colunas_sql}) FROM stdin DELIMITER ',' CSV HEADER;"


run_copy = f'psql -U postgres -d {database_name} -c "{copy_cmd}"'

process = subprocess.Popen(run_copy, shell=True, stdin=subprocess.PIPE)
process.communicate(input=csv_buffer.getvalue().encode('utf-8'))

print("Dados inseridos com sucesso!")