# Manual de Testes

Este documento explica como executar e manter os testes do analisador léxico.

## 🚀 Como Rodar os Testes

Fácil.

Instala com ```pip install pytest```.

Executa ```pytest``` na raiz pelo terminal. 

```pytest --tb=short``` para uma melhor visualização.


### Útil:
*   **Rodar apenas os testes de certo arquivo ou pasta:** `pytest Caminho/para/arquivo`
*   **Modo Detalhado (Verbose):** `pytest -v`
*   **Parar na primeira falha:** `pytest -x`

---

## ✍️ Como Escrever Novos Testes

Os testes utilizam o framework **pytest**. Para adicionar novos casos:

1.  **Padronização:** Todo arquivo de teste deve começar com `test_` (ex: `test_operadores.py`).
2.  **Parametrização:** Use o `@pytest.mark.parametrize` para testar vários inputs com a mesma lógica sem repetir código.

### Exemplo de Estrutura:
```python
# Testando se o texto lido foi tokenizado corretamente
@pytest.mark.parametrize("entrada", ["vaca", "frango"])
def test_palavras_reservadas(entrada):
    tokens = analisar_lexico(entrada)
    
    assert len(tokens) == 1 # Lista de tokens só pode ter 1 token
    assert tokens[0].texto == entrada # O texto do token deve ser o mesmo que foi lido
    assert tokens[0].tipo == "id" # O tipo do token de vaca e frango será id nessa situação
    assert tokens[0].linha == 0 # O token foi lido na linha 0
    
```

---

## 📊 Entendendo a Saída

Exemplo de saída:

```python
========= FAILURES =========
_________ test_soma[1-1] _________

teste_a = 1, teste_b = 1 // valores dos parametros escolhidos

    # Função testada
    @pytest.mark.parametrize("teste_a, teste_b", [(1,1)])
    def test_soma(teste_a, teste_b):
    
        resultado = soma(teste_a, teste_b)
    
>       assert resultado == teste_a + teste_b # teste feito
E       assert 3 == (1 + 1)                   # parâmetros

temp.py:12: AssertionError
========= short test summary info =========
FAILED temp.py::test_soma[1-1] - assert 3 == (1 + 1)
```
---
