#Q → Conjunto de estados.
#Σ → Alfabeto de entrada (conjunto de símbolos que a máquina pode ler).
#Γ → Alfabeto da pilha (símbolos que podem ser empilhados/desempilhados).
#δ → Função de transição: define para cada estado, símbolo de entrada, e símbolo do topo da pilha, qual a ação a ser tomada (novo estado e manipulação da pilha).
#q₀ → Estado inicial.
#Z₀ → Símbolo inicial da pilha.
#F → Conjunto de estados finais (opcional, depende se a aceitação é por estado ou esvaziamento da pilha).

from enum import Enum, auto #ajuda as enumerações - Padrao
from typing import List    #listar
from graphviz import Digraph #fazer imagemzinha

class Padrao(Enum):  #entende as entradas 
    SIMPLES = auto()
    REPETIDO = auto()
    OPCIONAL = auto()
    MULTIPLO = auto()
    INVERSO = auto()

class Segmento: #categorisa qual op é e o simbolo
    def __init__(self, categoria: Padrao, simbolo: str):
        self.categoria = categoria
        self.simbolo = simbolo

def decodificar_expressao(expressao: str) -> List[Segmento]:  #classificação dos simbolos e suas operacoes
    estrutura = []
    indice = 0
    while indice < len(expressao):
        if expressao[indice] == ' ':
            indice += 1
            continue
        caractere = expressao[indice]
        if indice + 2 < len(expressao) and expressao[indice + 1] == '^' and expressao[indice + 2] == 'n':
            estrutura.append(Segmento(Padrao.REPETIDO, caractere))
            estrutura.append(Segmento(Padrao.INVERSO, caractere))
            indice += 3
        elif indice + 1 < len(expressao) and expressao[indice + 1] == '*':
            estrutura.append(Segmento(Padrao.OPCIONAL, caractere))
            indice += 2
        elif indice + 1 < len(expressao) and expressao[indice + 1] == '+':
            estrutura.append(Segmento(Padrao.MULTIPLO, caractere))
            indice += 2
        else:
            estrutura.append(Segmento(Padrao.SIMPLES, caractere))
            indice += 1
    return estrutura

def mostrar_estrutura(estrutura: List[Segmento]):
    for bloco in estrutura:
        marca = {
            Padrao.SIMPLES: '',
            Padrao.REPETIDO: '^n',
            Padrao.OPCIONAL: '*',
            Padrao.MULTIPLO: '+',
            Padrao.INVERSO: '^n'
        }[bloco.categoria]
        print(f"{bloco.simbolo}{marca}", end=" | ")
    print()

def avaliar_sequencia(entrada: str, estrutura: List[Segmento], detalhado: bool = False) -> bool: #validação da sequencia
    cursor = 0
    suporte = []
    for etapa, bloco in enumerate(estrutura):
        if detalhado:
            print(f"[Etapa {etapa}] Posição: {cursor}, Suporte: {suporte}")
        if bloco.categoria == Padrao.OPCIONAL:
            while cursor < len(entrada) and entrada[cursor] == bloco.simbolo:
                if detalhado: print(f"Analisando opcional: {entrada[cursor]}")
                cursor += 1
        elif bloco.categoria == Padrao.MULTIPLO:
            if cursor >= len(entrada) or entrada[cursor] != bloco.simbolo:
                return False
            while cursor < len(entrada) and entrada[cursor] == bloco.simbolo:
                if detalhado: print(f"Analisando múltiplo: {entrada[cursor]}")
                cursor += 1
        elif bloco.categoria == Padrao.REPETIDO:
            while cursor < len(entrada) and entrada[cursor] == bloco.simbolo:
                if detalhado: print(f"Empilhando: {entrada[cursor]}")
                suporte.append(bloco.simbolo)
                cursor += 1
        elif bloco.categoria == Padrao.INVERSO:
            while suporte:
                if cursor >= len(entrada) or entrada[cursor] != bloco.simbolo:
                    return False
                if detalhado: print(f"Desempilhando: {entrada[cursor]}")
                suporte.pop()
                cursor += 1
        elif bloco.categoria == Padrao.SIMPLES:
            if cursor >= len(entrada) or entrada[cursor] != bloco.simbolo:
                return False
            if detalhado: print(f"Analisando simples: {entrada[cursor]}")
            cursor += 1
    if cursor == len(entrada):
        if detalhado: print("✅ Análise concluída com sucesso!")
        return True
    else:
        if detalhado: print("❌ Análise falhou!")
        return False

def gerar_diagrama(estrutura: List[Segmento], nome_saida='modelo_diagrama'): #gera um diagrama
    grafo = Digraph(comment='Representação Gráfica do Modelo')
    for pos, bloco in enumerate(estrutura):
        rotulo = f"{bloco.simbolo}"
        if bloco.categoria == Padrao.REPETIDO:
            rotulo += "^n"
        elif bloco.categoria == Padrao.OPCIONAL:
            rotulo += "*"
        elif bloco.categoria == Padrao.MULTIPLO:
            rotulo += "+"
        elif bloco.categoria == Padrao.INVERSO:
            rotulo += "^n"
        grafo.node(f's{pos}', f's{pos}')
        grafo.node(f's{pos + 1}', f's{pos + 1}')
        grafo.edge(f's{pos}', f's{pos + 1}', label=rotulo)
    grafo.render(filename=nome_saida, format='png', view=True)
