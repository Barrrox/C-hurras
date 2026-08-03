# 📝 TODO: Analisador Sintático (Bottom-Up SLR)

## 1. Gramática e Script Gerador (Desafio Principal)
- [ ] Revisar `docs/gramatica.txt` e adaptá-la para o formato SLR(1). É preciso adicionar uma regra inicial aumentada (ex: `<S'> -> <chs> EOF`).
- [ ] Criar o script auxiliar `gerador_slr.py` (ou similar) que:
  - Lê a gramática.
  - Calcula os conjuntos FIRST e FOLLOW.
  - Gera os itens LR(0) (conjuntos e fechamentos).
  - Constrói o autômato (transições entre os itens).
  - Monta as tabelas sintáticas `ACTION` e `GOTO`.
  - Salva ou exporta as tabelas para o analisador principal consumir (ex: JSON, pickle, ou apenas importa a estrutura de dados).

## 2. Refatoração do Analisador
- [ ] Descartar a base Top-Down de `analisador_sintatico.py` e preparar a lógica de um parser Bottom-Up genérico guiado por tabela.
- [ ] Garantir que a integração com o `analisador_lexico.py` se mantenha correta (lendo a lista de tokens e instanciando o parser).

## 3. Implementação do Algoritmo Shift-Reduce
- [ ] Implementar a pilha para rastrear **estados**.
- [ ] Implementar o loop de parsing (ler token da entrada, consultar estado do topo da pilha).
- [ ] Processar operação `Shift`: empilhar token e o novo estado correspondente.
- [ ] Processar operação `Reduce`: desempilhar a quantidade correspondente ao tamanho da regra, usar o não-terminal da redução para consultar a tabela `GOTO`, empilhar e ir para o novo estado.
- [ ] Processar `Accept`.

## 4. Tratamento de Erros (Modo Pânico)
- [ ] Adicionar a estratégia de tratamento de erro: ao se deparar com uma célula vazia (sem Ação definida), iniciar o Modo Pânico.
- [ ] Definir tokens de sincronização (ex: `;`, `}`).
- [ ] Executar a estratégia escolhida:
  1. Dar 'pop' (desempilhar) nos estados da pilha até encontrar um estado que possa efetuar um *Shift* em um dos tokens de sincronização.
  2. Descartar tokens da entrada iterativamente até encontrar esse token de sincronização.
  3. Retomar a análise para não travar no primeiro erro (conforme exigido pelo trabalho).

## 5. Testes Finais e Entrega
- [ ] Criar o arquivo fonte na linguagem C-Hurras contendo absolutamente todas as primitivas (if, while, declarações, atribuições).
- [ ] Rodar testes de estresse sintático: colocar erros de propósito no arquivo para validar o modo pânico.
