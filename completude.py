import pandas as pd

def verificar_dados_vazios(csv_files, output_report="relatorio_dados_vazios.txt"):
    """
    Verifica a quantidade de dados vazios em múltiplos arquivos CSV e gera um relatório.

    Args:
        csv_files (list): Lista de caminhos para os arquivos CSV.
        output_report (str): Caminho para o arquivo de relatório em formato TXT.
    """
    try:
        with open(output_report, "w", encoding="utf-8") as report:
            report.write("Relatório de Dados Vazios\n")
            report.write("=" * 30 + "\n\n")

            for csv_file in csv_files:
                report.write(f"Arquivo: {csv_file}\n")
                report.write("-" * 30 + "\n")

                # Ler o CSV
                df = pd.read_csv(csv_file, encoding='latin1', low_memory=False)

                # Verificar dados vazios por coluna
                total_vazios = df.isnull().sum()
                total_linhas = len(df)

                for coluna, vazios in total_vazios.items():
                    report.write(f"Coluna: {coluna}\n")
                    report.write(f"  Valores vazios: {vazios}\n")
                    report.write(f"  Percentual vazio: {vazios / total_linhas * 100:.2f}%\n\n")

                report.write("\n")

            print(f"Relatório gerado com sucesso: {output_report}")

    except FileNotFoundError as e:
        print(f"Erro: Um dos arquivos CSV não foi encontrado. {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# Exemplo de uso
csv_files = ["parte1.csv", "parte2.csv", "parte3.csv"]  # Substitua pelos nomes dos seus arquivos CSV
verificar_dados_vazios(csv_files)