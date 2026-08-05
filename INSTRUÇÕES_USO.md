# C-hurras

**Bah, o C-hurras é uma linguagem barril dobrado, pensada praquela gurizada tri bagual que gosta de assar uma costela e tomar um tchopssinho enquanto paleia com os códigos**

## Instruções de uso do Compilador:

Rode o comando ```python main.py <arquivo_codigo>```, em que arquivo_codigo é um arquivo de texto formatado em UTF-8. 

Em caso de uma leitura léxica bem-sucedida, a saída será mostrada no terminal como no exemplo a seguir:

```terminal 
python.exe .\main.py .\codigo_teste.txt
token: vaca | categoria: tipo | linha: 1
token: variavel1 | categoria: id | linha: 1
token: ; | categoria: ; | linha: 1
...
```

Em caso de falha, a saída será o primeiro erro léxico encontrado. Exemplo:

```terminal ERRO: Operador AND é: && na linha 4```

Exemplos de erros para testes:

1. Comentário mal aberto: --
2. Caractere vazio: ''
3. Caractere não fechado: 'a
4. String vazia ou inválida: "" ou "\n" ou "\n
5. AND incompleto: &
6. OR incompleto: |
7. Caracteres inválidos
