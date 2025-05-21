#Q → Conjunto de estados.
#Σ → Alfabeto de entrada (conjunto de símbolos que a máquina pode ler).
#Γ → Alfabeto da pilha (símbolos que podem ser empilhados/desempilhados).
#δ → Função de transição: define para cada estado, símbolo de entrada, e símbolo do topo da pilha, qual a ação a ser tomada (novo estado e manipulação da pilha).
#q₀ → Estado inicial.
#Z₀ → Símbolo inicial da pilha.
#F → Conjunto de estados finais (opcional, depende se a aceitação é por estado ou esvaziamento da pilha).

from graphviz import Digraph


class AutomatoAPilha:
    def __init__(self): #inicio todos os estado : estado final, estado final , e um auxiliar 
        self.pilha = ['Z'] #tecnicamente eu só vou manipular o Z e o A então poderia ser Alfabeto da pilha 
        self.estado_atual = 'q0' #estado inicial 
        self.estados_finais = {'qf'}#estado final
        self.estados = {'q0', 'q1'} #conjunto de estado s

    def transicao(self, simbolo): #para transiciionar os estados -> funcao de transicao 
        print(f"Estado atual: {self.estado_atual}, símbolo lido: '{simbolo}', pilha: {self.pilha}")

        if self.estado_atual == 'q0':
            if simbolo == 'a': #quando le a empilha A
                self.pilha.append('A')
                print(f"Empilhou 'A' → Pilha: {self.pilha}")
            elif simbolo == 'b': #quando le b joga pro q1
                self.estado_atual = 'q1'
                print(f"Transição para estado 'q1'")
                self.transicao(simbolo)
            else: 
                print(f"Símbolo inválido '{simbolo}' em estado 'q0'")

        elif self.estado_atual == 'q1': # pra quando tiver um A no topo ele desempilha
            if simbolo == 'b':
                if self.pilha and self.pilha[-1] == 'A':
                    self.pilha.pop()
                    print(f"Desempilhou 'A' → Pilha: {self.pilha}")
                else:
                    print(f"Erro: Tentativa de desempilhar 'A', mas pilha = {self.pilha}")
            else:
                print(f"Símbolo inválido '{simbolo}' em estado 'q1'")

    def processar_entrada(self, cadeia):
        print(f"\nProcessando cadeia: {cadeia}")

        for simbolo in cadeia: #processar cada simbolo
            self.transicao(simbolo)

        if self.estado_atual == 'q1' and self.pilha == ['Z']:
            self.estado_atual = 'qf'
            print("✅ Cadeia aceita!")
        else:
            print("❌ Cadeia rejeitada.")


def desenhar_automato(): # função para desenhar o autômato 
    dot = Digraph()

    # Estados
    dot.node('q0', shape='circle')
    dot.node('q1', shape='circle')
    dot.node('qf', shape='doublecircle') # estado final com duplo círculo

    # Transições
    dot.edge('q0', 'q0', label='a; empilha A')
    dot.edge('q0', 'q1', label='b; transita')
    dot.edge('q1', 'q1', label='b; desempilha A')

    # Indicar o estado inicial
    dot.edge('', 'q0', label='início')


    dot.render('automato_pilha', view=True, format='png')


if __name__ == "__main__":
    desenhar_automato() # desenha o autômato antes de processar a cadeia

    aap = AutomatoAPilha()

    cadeia = input("Digite a cadeia que deseja processar (ex: 'aaabbb'): ").strip()

    if all(c in {'a', 'b'} for c in cadeia): #essa validação pode servir como alfabeto de entrada? sim né?
        aap.processar_entrada(cadeia)
    else:
        print("A cadeia só pode conter os símbolos 'a' e 'b'.")
