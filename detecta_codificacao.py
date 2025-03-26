import chardet

def detectar_codificacao(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

caminho_arquivo = 'SIHAIH_utf8_convertido.csv'
codificacao = detectar_codificacao(caminho_arquivo)

if codificacao:
    print(f"A codificação detectada é: {codificacao}")
else:
    print("Não foi possível detectar a codificação.")