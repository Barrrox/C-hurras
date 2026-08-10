# Rascunho de Arquitetura: Analisador Sintático SLR(1)

Classes, divisão de responsabilidades das classes e ideia para o fluxo de processamento. Alguns nomes/labels podem estar diferentes no código, na imagem e nos textos abaixo. 

![diagrama](../assets/arquitetura.png)

## 1. Arquitetura de Classes Proposta

O projeto é dividido em dois ecossistemas: o gerador offline (que processa a gramática) e o compilador online (que consome a tabela gerada).

### Ecossistema 1: O Gerador SLR (`src/construtor_tabelaSLR.py`)
Roda apenas quando a linguagem/gramática sofrer alterações para recalcular o cérebro do analisador.

*   **`Gramatica`**:
    *   **Responsabilidade**: Ler e carregar o arquivo JSON com as regras (`regras_producao.json`). Sendo a única fonte da verdade da gramática.
    *   **Métodos Principais**: `calcular_first()`, `calcular_follow()`. Identifica terminais e não-terminais.
*   **`ItemLR`**:
    *   **Responsabilidade**: Estrutura simples para representar um item do autômato (ex: `<S'> -> . <chs>`). Guarda a regra, o lado esquerdo e a posição do "ponto" (dot) de transição.
*   **`AutomatoLR0`**:
    *   **Responsabilidade**: Processar a `Gramatica` gerando todos os itens validos.
    *   **Métodos Principais**: `closure(item)`, `goto(estado, simbolo)`. Gera todos os estados possíveis.
*   **`ConstrutorTabelaSLR`**:
    *   **Responsabilidade**: Unir o Autômato e os conjuntos Follow para gerar a tabela.
    *   **Métodos Principais**: `construir_tabelaSLR()`, `exportar_json()` (salva a matriz final no arquivo `tabela_slr.json`).

### Ecossistema 2: O Compilador Principal (Orquestrador)
É a esteira principal que roda quando queremos compilar um código da linguagem `C-Hurras`.

*   **`Token`**:
    *   **Responsabilidade**: Classe de modelo simples. Guarda string, categoria e linha.
*   **`Lexer`** (em `src/analisador_lexico.py`):
    *   **Responsabilidade**: Fazer varredura de caracteres.
    *   **Métodos Principais**: `__init__()`, `analisar_lexico(codigo)`.
*   **`ParserSLR`** (em `src/analisador_sintatico.py`):
    *   **Responsabilidade**: O núcleo da Fase 2. Uma máquina orientada a pilha e tabela.
    *   **Métodos Principais**: 
        *   `__init__()`: Inicializa carregando a classe `Gramatica` (para saber o tamanho das reduções) e carrega as tabelas prontas.
        *   `analisar_sintaxe(lista_tokens)`: O loop principal Shift-Reduce.
        *   `modo_panico(token_atual)`: (Modo Pânico)

---

## 2. Sequência de Chamadas (Fluxo de Execução)

O fluxo de dados ao compilar um código fonte (ex: `codigo.churras`):

1.  **Pré-requisito**: O arquivo de tabelas (`tabela_slr.json`) já foi gerado offline por `src/construtor_tabelaSLR.py`.
2.  **Início**: O arquivo principal (`main.py`) lê o código-fonte em texto do arquivo `.churras` e instancia a classe `Compilador`.
3.  **Orquestração (`Compilador`)**:
    *   Instancia `lexer = Lexer()` e `parser = ParserSLR()`.
    *   Chama `compilar(codigo)`.
4.  **Chamada Léxica**:
    *   Chama `lista_tokens = lexer.analisar_lexico(codigo)`.
    *   O retorno é um array/lista de objetos `Token`. Erros léxicos são relatados aqui.
5.  **Chamada Sintática**:
    *   Inicia a análise passando a fita léxica: `parser.analisar_sintaxe(lista_tokens)`.
6.  **Loop Shift-Reduce (`analisar_sintaxe()`)**:
    *   O Parser inicia a Pilha de Estados colocando `[ 0 ]`.
    *   Para cada token na `lista_tokens`:
        *   `estado_topo = pilha[-1]`
        *   Consulta na tabela: `acao = tabelaSLR[estado_topo][token.categoria]`.
        *   Se `acao` == **Shift(N)**: Coloca o token e o Estado **N** na pilha. Avança a fita de tokens.
        *   Se `acao` == **Reduce(Regra)**: Desempilha instâncias da pilha baseado no tamanho da regra. Consulta a tabela SLR usando o estado remanescente no topo e o Não-Terminal reduzido. Empilha o novo estado. *A fita do token **não** avança nesta operação.*
        *   Se `acao` == **Accept**: Sucesso! O código está sintaticamente correto. Fim do laço.
        *   Se `acao` == **Erro**: Aciona o Modo Pânico.
7.  **Recuperação de Erros (Modo Pânico)**
8.  **Fim do Programa**: Relatório de status é impresso para o usuário indicando as falhas reportadas ou o sucesso pleno.
