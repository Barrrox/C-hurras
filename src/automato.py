import json
import os

from gramatica import Gramatica


class ItemLR:
    def __init__(self, esquerda_producao: str, direita_producao: tuple[str], ponto: int = 0) -> None:
        self.esq: str = esquerda_producao
        self.dir: tuple[str] = direita_producao
        self.ponto: int = ponto # Começa em 0


        # Deixar alocado o simbolo apos o ponto.
        if self.ponto < len(self.dir): # Se ponto antes do fim
            self.ponto_dir = self.dir[self.ponto]

        elif self.ponto == len(self.dir): # Se ponto no fim ou self.dir = [], não há nada depois do ponto
            self.ponto_dir = None
        else:
            print("Erro em ItemLR: a posição do ponto ultrapassa o index da parte direita do item")
            exit()
        
    # Método para printar Item no terminal para debug manual
    def imprimir(self) -> None:
        print(self.esq, "->", self.dir)

        # Como aloca:
            #  T → • T * F: ItemLR(esquerda, direita, 0)
            #  T → T * • F: ItemLR(T, [T,*,F], 2)

        # Operações:
            # Símbolo após o ponto: dir[ponto] -> da pra deixar alocado já que os itens são estáticos
            # É item de redução? ponto == len(direita)
            # Desvio (avançar o ponto): ItemLR(esquerda, direita, ponto + 1)

class Estado:

    def __init__(self, id : int,
                 fechamento : list['ItemLR']) -> None:
        self.id : int = id
        self.fechamento : list['ItemLR'] = fechamento


class AutomatoLR0:
    def __init__(self, gramatica: Gramatica) -> None:
        """ Recebe a gramatica já lida e processada """

        self.estados : list[Estado] = []    # Lista contendo os conjuntos de Itens LR(0)
        self.transicoes : dict[tuple[int, str], int] = {} # Mapeia: (estado_origem, simbolo) -> estado_destino

        # self.gerar_automato(gramatica) # Gera o automato 
    
    def get_item_inicial(self, gramatica: Gramatica) -> ItemLR:
        """Pega o item inicial da gramática 

        Args:
            gramatica (Gramatica): A instância da gramática lida.

        Returns:
            ItemLR: O item inicial do autômato (com ponto 0)
        """
        producao_incial = gramatica.producoes[0]
        return ItemLR(producao_incial[0], producao_incial[1], 0)
    
    def achar_producao_no_automato(self, item : ItemLR) -> int:
        """
            TODO: barros, enfeita esse método bem aqui <--
        """
        for estado in self.estados:
            for item_do_estado in estado.fechamento:
                if item == item_do_estado:
                    return estado.id
        return -1

    def gerar_automato(self, gramatica : Gramatica) -> None:
        """
        estado inicial
        realiza fechamento

        para cada estado ainda não processado:
            calcular todos os símbolos lidos
            incluir diferentes produções de mesma leitura no mesmo vetor?
            para cada leitura:
                checar em todos os estados do autômato se produção com desvio existe
                se existir:
                    criar transição sob símbolo para esse estado
                caso contrario:
                    criar estado novo
                    criar transição sob símbolo para esse novo estado
                    colocar todas as produções com o símbolo lido
                    realizar fechamento
        """
        id_counter = 0
        fila_estados = list[Estado(id_counter, self.fechamento([self.get_item_inicial()], gramatica))]
        
        # Para todos os estados
        while fila_estados:
            estado = fila_estados.pop(0)
            estados.append(estado)
            
            # Para cada produção do fechamento do estado
            for item in estado.fechamento:
                # Realiza desvio do item
                item_desviado = ItemLR(item.esq, item.dir, item.ponto+1)
                
                # Checa de produção desviada na existe
                estado_alvo = achar_producao_no_automato(item_desviado)
                
                # Se produção existe
                if estado_alvo >= 0 and ([(estado.id, item.ponto_dir), estado_alvo] not in self.transicoes):
                    # Adicionar ponteiro pro novo estado
                    self.transicoes.append([(estado.id, item.ponto_dir), estado_alvo])

                # Se produção não existe, criar estado
                else:
                    # Calcula desvio_estado
                    fechamento_estado_novo = desvio_estado(estado.fechamento, item.ponto_dir)
                    
                    # Cria estado novo
                    id_counter += 1
                    self.estados.append(Estado(id_counter, fechamento_estado_novo))
                    
                    # Adicionar ponteiro pro novo estado
                    self.transicoes.append([(estado.id, item.ponto_dir), id_counter])

        # 2. Criar conjunto de itens inicial da gramatica


    """
    Operação de Fechamento
    - Considere I como o conjunto de itens para G
    - O fechamento(I) é o conjunto de itens construídos a partir de I
    - Regras:
        1)Cada item em I é adicionado ao fechamento(I)
        2)Se A → a•Bb estiver em fechamento(I) e B → c for uma produção, adicionar o item B → •c ao conjunto I
    - Repete-se até que não se possa mais adicionar novos itens

    Exemplo:
    Dada a gramática:
    E'→ E
    E → E + T | T
    T → T*F | F
    F → (E) | id
    Se I for o conjunto de um
    item {[E' → •E]}, então

    fechamento(I) = {
    E' → E {ponto de partida - R1}
    E → •E + T
    E → •T
    T → •T*•F
    T → •F
    F → •(E)
    F → •id

    """ 
    def fechamento(self, I: list[ItemLR], producoes : tuple[tuple[str, tuple[str]]]) -> list[ItemLR]:
        """Expande o fechamento de I. Trabalha um pouco diferente sobre o conjunto I de como é tratado nos slides: Torna I uma fila para auxiliar no processo. Logo, passar cópia de I como parâmetro

        Args:
            I (list[ItemLR]): Cópia do conjunto de itens iniciais.
            producoes (tuple): As produções da gramática para verificar transições vazias.

        Returns:
            list[ItemLR]: fechamento de I
        """

        fechamento : list[ItemLR] = []
        
        # 1) Cada item em I é adicionado ao fechamento(I)
        # Uso um while aqui pois I vai crescer (for não funciona) e vou retirar os itens já verificados de I
        # enquanto adiciono novos itens a serem verificados. Quanto I acabar, todos os itens já foram verificados
        simb_adicionados_I = [] # Lista com símbolos de produções que já foram adicionados à I
        # procurar na gramática o index de todas as produções de I
        for i in range(len(I)):
            item = I[i]
            for j in range(len(producoes)):
                prod = producoes[j]
                if item.esq == prod[0] and item.dir == prod[1]:
                    simb_adicionados_I.append(j)

        while I:
            item = I.pop(0) # Começo da fila
            fechamento.append(item)
            #print(simb_adicionados_I)
            #print()
            #print()

            # 2) Se A → a•Bb estiver em fechamento(I) e B → c for uma produção de I, adicionar o item B → •c ao conjunto I
            for i in range(len(producoes)): # Loop para procurar produção B → c na gramática -> O(n^2), talvez precise otimizar aqui
                
                if i in simb_adicionados_I: # SE simbolo já foi analisado completamente
                    continue
                
                producao = producoes[i]
                
                # Produção convertida para item
                prod_item = ItemLR(esquerda_producao=producao[0], 
                                   direita_producao=producao[1], 
                                   ponto=0)
            
                # se (o simbolo a direita do ponto de item) é (o primeiro de alguma produção da gramática) então (adiciona à I)
                if item.ponto_dir == producao[0]: # 
                    I.append(prod_item)
                    simb_adicionados_I.append(i)


        return fechamento



    """ 4) Operação de Desvio
    
    - Desvio(I,X)
        ● Conjunto de itens I e um símbolo X
        ● Retorna um conjunto de itens
    - Cálculo do desvio a partir do estado I ao ler X:
        ● Mover ponto para direita em todos os itens de I onde o ponto precede X
    - Para todas as regras A → α•Xβ em C, retorna A → αX•β
        ● Calcular o fechamento deste conjunto de itens
    """
    
    def desvio_estado(self, I: list[ItemLR], X: str) -> list[ItemLR]:
        novo_conjunto_itens = []

        # Mover ponto para diereita em todos os itens de I onde o ponto precede X
        for item in I:
            # Verifica se o símbolo logo após o ponto é o símbolo X que estamos lendo
            if item.ponto_dir == X:
                # Retorna A → αX•β (cria um novo item com o ponto avançado em 1)
                novo_item = ItemLR(esquerda_producao=item.esq,
                                   direita_producao=item.dir,
                                   ponto=item.ponto + 1)

                novo_conjunto_itens.append(novo_item)

        # Retorna o fechamento deste novo conjunto de itens
        return self.fechamento(novo_conjunto_itens, producoes)



    def exportar_json(self, caminho: str = "automato.json") -> None:
        """Lê os estados e transições e salva o automato em um JSON
        """

        # Estrutura o JSON para salvar os estados e transições do autômato
        estados_json = []
        for estado in self.estados:
            itens_json = []
            
            # Converte os objetos ItemLR para dicionários puros
            for item in estado.fechamento:
                itens_json.append({
                    "esq": item.esq,
                    "dir": list(item.dir),  # Converte tupla para lista para compatibilidade JSON
                    "ponto": item.ponto
                })
                
            estados_json.append({
                "id": estado.id,
                "fechamento": itens_json
            })

        # Estrutura as transições do autômato
        # Converte o dicionário {(origem, simbolo): destino} em uma lista de transições
        transicoes_json = []
        for (origem, simbolo), destino in self.transicoes.items():
            transicoes_json.append({
                "origem": origem,
                "simbolo": simbolo,
                "destino": destino
            })

        # Monta o dicionário final que será salvo
        dados_automato = {
            "estados": estados_json,
            "transicoes": transicoes_json
        }

        # Escreve o JSON
        try:
            diretorio = os.path.dirname(caminho)
            if diretorio:
                os.makedirs(diretorio, exist_ok=True)
                
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados_automato, f, indent=4, ensure_ascii=False)
                
            print(f"Automato salvo com sucesso em: {caminho}")
            
        except Exception as e:
            print(f"ERRO ao salvar o automato: {e}")
