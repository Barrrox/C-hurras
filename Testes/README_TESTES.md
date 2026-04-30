# Manual de Testes - C-Hurras

Este documento explica como executar e manter os testes do analisador léxico.

## 🚀 Como Rodar os Testes

Certifique-se de ter o `pytest` instalado:
```bash
pip install pytest
```

Execute na raiz do projeto:
```bash
pytest --tb=short
```

---

## ✍️ Como Escrever Novos Testes

Para evitar retrabalho e acoplamento, utilize as funções utilitárias em `testes/utils.py`.

### Funções Disponíveis:
*   `executar_lexico(codigo)`: Chama o analisador léxico.
*   `validar_token(token, texto, categoria)`: Valida se o token tem o conteúdo esperado.
*   `verificar_erro_lexico(codigo)`: Garante que um código inválido dispara um erro.

### Exemplo de Estrutura Ideal:
```python
from testes.utils import executar_lexico, validar_token

def test_exemplo_id():
    tokens = executar_lexico("vaca")
    assert len(tokens) == 1
    validar_token(tokens[0], "vaca", "tipo") # 'vaca' é da categoria 'tipo' (variável)
```

---

## 🏗️ Estrutura de Pastas
*   `unitarios/`: Testes de tokens isolados (números, strings, IDs).
*   `integracao/`: Testes de múltiplos tokens e interações sem espaço ("colados").
*   `utils.py`: Camada de abstração para evitar acoplamento.
