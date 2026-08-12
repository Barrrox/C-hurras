import json
import os

from gramatica import Gramatica


class ItemLR:
    def __init__(self, esquerda_producao: str, direita_producao: tuple[str], ponto: int = 0) -> None:
        self.esq: str = esquerda_producao
        self.dir: tuple[str] = direita_producao
        self.ponto: int = ponto # Começa em 0
        

        # Se for uma produção para vazio, ja está finalizada
        if self.dir[0] == "~":
            self.ponto = 1
            self.ponto_dir = None
        # Deixar alocado o simbolo apos o ponto.
        elif self.ponto < len(self.dir): # Se ponto antes do fim
            self.ponto_dir = self.dir[self.ponto]

        elif self.ponto == len(self.dir): # Se ponto no fim ou self.dir = [], não há nada depois do ponto
            self.ponto_dir = None
        else:
            print("Erro em ItemLR: a posição do ponto ultrapassa o index da parte direita do item")
            exit()

    def __eq__(self, other) -> bool:
        if not isinstance(other, ItemLR):
            return NotImplemented
        return (self.esq == other.esq and
                self.dir == other.dir and
                self.ponto == other.ponto)

    def __hash__(self) -> int:
        # Necessário apenas se for usar conjuntos ou dicionários com ItemLR como chave
        return hash((self.esq, self.dir, self.ponto))
    
    # Método para printar Item no terminal para debug manual
    def imprimir(self) -> None:
        print(self.esq, "->", self.dir, "PONTO:", self.ponto)

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
        
    def __eq__(self, other) -> bool:
        if not isinstance(other, Estado):
            return NotImplemented
        # Estados são iguais se possuem o mesmo conjunto de itens (ordem irrelevante)
        return frozenset(self.fechamento) == frozenset(other.fechamento)

    def __hash__(self) -> int:
        # Hash baseado apenas no conjunto de itens (frozenset), ignorando o id
        return hash(frozenset(self.fechamento))


class AutomatoLR0:
    def __init__(self, gramatica: Gramatica) -> None:
        """ Recebe a gramatica já lida e processada """

        self.estados : list[Estado] = []    # Lista contendo os conjuntos de Itens LR(0)
        self.transicoes : dict[tuple[int, str], int] = {} # Mapeia: (estado_origem, simbolo) -> estado_destino

        #self.gerar_automato(gramatica) # Gera o automato 
    
    def get_item_inicial(self, gramatica: Gramatica) -> ItemLR:
        """Pega o item inicial da gramática 

        Args:
            gramatica (Gramatica): A instância da gramática lida.

        Returns:
            ItemLR: O item inicial do autômato (com ponto 0)
        """
        producao_incial = gramatica.producoes[0]
        return ItemLR(producao_incial[0], producao_incial[1], 0)

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
        fila_estados = [Estado(id_counter, self.fechamento([self.get_item_inicial(gramatica)], gramatica.producoes))]
        self.estados.append(Estado(id_counter, self.fechamento([self.get_item_inicial(gramatica)], gramatica.producoes)))
        id_counter += 1
        
        # Para todos os estados
        while fila_estados:
            #print("Fila de estados:")
            #for est in fila_estados:
            #    print(est.id)
            #print("---------------")
            estado = fila_estados.pop(0)
            
            # Listar todos os simbolos lidos
            leituras = []
            for item in estado.fechamento:
                if (item.ponto_dir not in leituras) and (item.ponto_dir != None):
                    leituras.append(item.ponto_dir)
            
            # Para cada leitura
            for leitura in leituras:
                
                # Construir possível estado novo
                fechamento_estado_novo = self.desvio_estado(estado.fechamento, leitura, gramatica.producoes)
                estado_novo = Estado(id_counter, fechamento_estado_novo)
                id_counter += 1
                
                # Se estado ja existir
                estado_alvo = -1
                for i in range(len(self.estados)):
                    est = self.estados[i]
                    if estado_novo == est:
                        estado_alvo = i
                if estado_alvo >= 0:
                    self.transicoes[(estado.id, leitura)] = estado_alvo
                    id_counter -= 1
                    
                # Se estado ainda não existir
                else:
                    fila_estados.append(estado_novo)
                    self.estados.append(estado_novo)
                    
                    # Adicionar ponteiro pro novo estado
                    self.transicoes[(estado.id, leitura)] = id_counter
                


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
        prod_adicionados_I : list[ItemLR] = I.copy() # Lista com símbolos de produções que já foram adicionados à I
        #print("PROCESSANDO ESTADO:")
        #for i in I:
        #    i.imprimir()

        while I:
            item = I.pop(0) # Começo da fila
            fechamento.append(item)

            # 2) Se A → a•Bb estiver em fechamento(I) e B → c for uma produção de I, adicionar o item B → •c ao conjunto I
            for i in range(len(producoes)): # Loop para procurar produção B → c na gramática -> O(n^2), talvez precise otimizar aqui
                
                producao = producoes[i]
                
                # Produção convertida para item
                prod_item = ItemLR(esquerda_producao=producao[0], 
                                   direita_producao=producao[1], 
                                   ponto=0)
                
                #print("-----------------------------------------")
                #print("COMPARANDO:")
                #prod_item.imprimir()
                #print("ESTA EM:")
                #for j in prod_adicionados_I:
                #    j.imprimir()
                #print("-----------------------------------------\n")
                
                if prod_item in prod_adicionados_I: # SE produção já foi adicionada completamente
                    continue
            
                # se (o simbolo a direita do ponto de item) é (o primeiro de alguma produção da gramática) então (adiciona à I)
                if item.ponto_dir == producao[0]: # 
                    I.append(prod_item)
                    prod_adicionados_I.append(prod_item)

        #print("ESTADO PROCESSADO:")
        #for i in fechamento:
        #    i.imprimir()
        #print("---------------------")
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
    
    def desvio_estado(self, I: list[ItemLR], X: str, producoes) -> list[ItemLR]:
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




mega = Gramatica("gramatica_teste_manual.json")
automato = AutomatoLR0(mega.producoes)
resultado = automato.gerar_automato(mega)
for estado in automato.estados:
    print("Estado I -", estado.id)
    print("PRODUÇÕES:")
    for i in estado.fechamento:
        i.imprimir()
    print()
    print("---------------------------------")
    print()
