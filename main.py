import sys
import os

# Adiciona o diretório src/ ao sys.path para que os imports funcionem
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from compilador import compilador

# 1. le o arquivo de código e retorna como um vetor de caracteres
def ler_arquivo(caminho_codigo):
    with open(caminho_codigo, "r") as arquivo:
        codigo = arquivo.read()
    return codigo



def main():

    if len(sys.argv) != 2:
        print("ERRO: arquivo não informado, use o analisador como:\n\tpython analisador_lexico.py codigo.churras")
        return

    # 1. le o arquivo de código e retorna como a string do código como foi lida
    codigo = ler_arquivo(sys.argv[1])

    churras = compilador()
    
    churras.compilar(codigo=codigo)

    

   

if __name__ == "__main__":
    main()