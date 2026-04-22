# Manual de Testes

Este documento explica como executar e manter os testes do analisador léxico.

## 🚀 Como Rodar os Testes

Para rodar todos os testes (estando na raiz do projeto) com a melhor visualização e mensagens de erro curtas, utilize:

```powershell
pytest --tb=short
```

### Comandos Úteis:
*   **Rodar apenas os testes do lexer:** `pytest --tb=short Testes/teste_analisador_lexico.py`
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

Com o `pytest-sugar` instalado:

*   **Barra de Progresso:** Indica o avanço total dos testes em tempo real.
*   **✓ (Passed):** O teste passou conforme o esperado.
*   **⨯ (Failed):** O teste falhou e o erro será exibido imediatamente abaixo.
*   **s (Skipped):** O teste foi ignorado.

---
*Nota: Recomenda-se adicionar um espaço " " ao final da string de entrada nos testes manuais para garantir que o lookahead do lexer processe corretamente o último token.*
