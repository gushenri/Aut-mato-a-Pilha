from pilhando import decodificar_expressao, mostrar_estrutura, avaliar_sequencia, gerar_diagrama, Padrao

def exibir_ajuda():
    print("""
==== Guia: Utilização do Analisador Sequencial ====

Símbolos suportados:
- ^n : repetição com memória (empilha e desempilha), ex.: a^n b^n
- *  : zero ou mais ocorrências, ex.: a*
- +  : uma ou mais ocorrências, ex.: a+

Exemplo de modelo: a^n b+ c^n
Exemplo de sequência: aaabbbccc

==============================================
""")

def exibir_estrutura_explicativa(estrutura):
    print("\n📋 Estrutura processada (explicada):")
    for idx, bloco in enumerate(estrutura):
        tipo = bloco.categoria
        if tipo == Padrao.SIMPLES:
            descricao = "ocorrência única"
        elif tipo == Padrao.REPETIDO:
            descricao = "repetição com empilhamento (^n)"
        elif tipo == Padrao.INVERSO:
            descricao = "desempilhamento espelhado (^n)"
        elif tipo == Padrao.OPCIONAL:
            descricao = "zero ou mais vezes (*)"
        elif tipo == Padrao.MULTIPLO:
            descricao = "uma ou mais vezes (+)"
        else:
            descricao = "desconhecido"
        print(f" {idx + 1}. Símbolo: '{bloco.simbolo}' → {descricao}")

exibir_ajuda()

while True:
    modelo = input("Especifique o modelo (ou '?' para ajuda): ").strip()
    if modelo == '?':
        exibir_ajuda()
        continue
    if modelo:
        break
    print("⚠️ O modelo não pode ser vazio. Por favor, informe um valor.")

while True:
    sequencia = input("Especifique a sequência a ser verificada: ").strip()
    if sequencia:
        break
    print("⚠️ A sequência não pode ser vazia. Por favor, informe um valor.")

print(f"\n✅ Modelo recebido: {modelo}")
print(f"✅ Sequência recebida: {sequencia}")
confirmar = input("Deseja prosseguir? (s/n): ").strip().lower()
if confirmar not in ('s', 'sim'):
    print("❌ Processo cancelado pelo usuário.")
    exit()

elementos = decodificar_expressao(modelo)

exibir_estrutura_explicativa(elementos)

gerar_diagrama(elementos)

detalhado = input("Ativar modo detalhado de análise? (s/n): ").strip().lower() in ('s', 'sim')

valido = avaliar_sequencia(sequencia, elementos, detalhado=detalhado)

print("\n🎯 Resultado:", "✅ SEQUÊNCIA ACEITA!" if valido else "❌ SEQUÊNCIA REJEITADA!")
