import numpy as np
from gramatica import Gramatica
from automato import AutomatoLR0

class SLRcell:
    def __init__(self, tipo, valor):
        """Célula da tabela SLR, representando uma ação ou transição

        Args:
            tipo (int): Tipo da ação. 0=empilha, 1=reduz, 2=aceita, 3=erro(vazio), 4=erro(reduz), 5=goto
            valor (int): Valor numérico associado à ação (estado alvo ou índice da produção)
        """
        self.tipo = tipo   # empilha, reduz, aceita, errovazio, erroreduz, goto -> 0, 1, 2, 3, 4, 5
        self.valor = valor # valor numerico referente a acao

class ConstrutorTabelaSLR:

    def __init__(self):
        """Inicializa o ConstrutorTabelaSLR com estruturas de dados vazias.
        A construção efetiva da tabela é feita chamando construir_tabelaSLR(gramatica, automato).
        """

        # Estruturas alvo (vão pro JSON e pro Parser)
        self.tabelaSLR = {}
        self.regras = {} # Regras de produção da gramática

    def construir_tabelaSLR(self, gramatica : Gramatica, automato : AutomatoLR0) -> None:
        """Constrói a tabela SLR
        """

        """
        O que faz:
        1. Varre estados do self.automato.
        2. Aplica lógica SLR(1) usando self.gramatica.follow_sets.
        3. Preenche self.tabelaSLR (com Shift, Reduce, Accept, Erro).
        4. Formata self.regras (ID -> {lhs, tamanho}).

        O que retorna: Nada. Altera atributos de instância.
        """
        
        """
        Entrada: Gramática aumentada G’
        Saída: Funções sintáticas SLR ação e desvio para G’
        Proc tabela(G’)
        {
            1. Construir C = {I0, I1, ..., In}   // coleção de itens LR(0) para G’
            2. O estado i é construído a partir de Ii. As ações sintáticas para o estado i são determinadas como segue:
                a) Se [A → α•aβ] está em Ii e desvio(Ii, a) = Ij, então fazer ação[i, a] = “empilha j”. Aqui a é um terminal.   // R1
                b) Se [A → α•] está em Ii, então fazer ação[i, a] = “reduzir A → α” para todo a ∈ Follow(A). Aqui A ≠ S’.   // R2
                c) Se [S’ → S•] está em Ii, então fazer ação[i, $] = “aceitar”.   // R3
            3. As transições de desvio para o estado i são construídas para todos os não-terminais A usando a regra: se desvio(Ii, A) = Ij, então desvio[i, A] = j.   // R4
            4. Entradas não definidas nas tabelas correspondem a erro.
        }
        """

        # Inicializar tabela SLR com N linhas (N estados do automato) e com T + A colunas (T terminais + A não terminais -> Seguindo regra 4 dos slides na construção da tabela)
        tabelaSLR = [[SLRcell(3, 0) for _ in range(len(gramatica.simbolos))] for _ in range(len(automato.estados))]
        
        
        # Para cada estado
        for estado in automato.estados:
            # Para cada produção
            for item in estado.fechamento:
                # Obtem simbolo lido
                simbolo_lido = item.ponto_dir
                producao = (item.esq, item.dir)
                
                # Se lê um terminal
                if simbolo_lido in gramatica.terminais:
                    # Coloca em tabela[estado, terminal] um empilhar estado_alvo
                    tabelaSLR[estado.id][gramatica.simbolos[simbolo_lido]] = SLRcell(0, automato.transicoes[(estado.id, simbolo_lido)])
                    
                # Se o ponto_dir == None e também é a produção 0 da gramatica
                elif (simbolo_lido == None) and (producao == gramatica.producoes[0]):
                    # Coloca em tabela[estado, $] o aceita
                    tabelaSLR[estado.id][gramatica.simbolos['$']] = SLRcell(2, -1)
                    
                # Se o ponto_dir == None
                elif (simbolo_lido == None):
                    # Coloca no follow de gramatica.esq da produção a redução (própria produção)
                    producao_index = -1
                    for i in range(len(gramatica.producoes)):
                        prod = gramatica.producoes[i]
                        if prod == producao:
                            producao_index = i
                            break
                    for flw in gramatica.follow[item.esq]:
                        tabelaSLR[estado.id][gramatica.simbolos[flw]] = SLRcell(1, producao_index)
                    
                # Se lê um não-terminal
                elif simbolo_lido in gramatica.nao_terminais:
                    # Coloca em tabela[estado, não-terminal] o goto estado_alvo
                    tabelaSLR[estado.id][gramatica.simbolos[simbolo_lido]] = SLRcell(5, automato.transicoes[(estado.id, simbolo_lido)])
                
                # Se isso rodar, algo deu errado
                else:
                    print("a tabela não ta indo, ta lendo coisa que não devia, suspeito...")
                    return
        
        self.tabelaSLR = tabelaSLR

        return tabelaSLR

    def exportar_json(self, caminho : str = "tabela_slr.json") -> None:
        """Salva a tabela SLR e as regras de produção em formato JSON

        Args:
            caminho (str): Caminho do arquivo de saída. Default: 'tabela_slr.json'
        """
        pass

# if __name__ == "__main__":
#     ntop = {
#         0: 'E',
#         1: 'R',
#         2: 'A',
#         5: 'G',
#         3: '~'
#     }

#     mega = Gramatica("gramatica_teste_manual.json")
#     automato = AutomatoLR0()
#     resultado = automato.gerar_automato(mega)
#     tabelador = ConstrutorTabelaSLR()
#     tabelador.construir_tabelaSLR(mega, automato)
#     tabela = tabelador.tabelaSLR

#     for estado in automato.estados:
#         print("Estado I -", estado.id)
#         print("PRODUÇÕES:")
#         for i in estado.fechamento:
#             i.imprimir()
#         print()
#         print("---------------------------------")
#         print()


#     simbolos_inv = {v: k for k, v in mega.simbolos.items()}
#     for col in range(len(tabela[0])):
#         print(simbolos_inv[col], ", ", end="")
#     print()
#     for lin in range(len(tabela)):
#         for col in range(len(tabela[0])):
#             print(ntop[tabela[lin][col].tipo], tabela[lin][col].valor, ", ", end="")
#         print()