
# - Cadastrar, Editar ou Remover produtos dinamicamente, considerar um modo administrador.

produtos = [['ID', 'Produto', 'Valor', 'Estoque'],
            [1, '-Coca-cola', 3.75, 2],
            [2, '---Pepsi--', 3.67, 5],
            [3, '--Monster-', 9.96, 1],
            [4, '---Café---', 1.25, 100],
            [5, '--Redbull-', 13.99, 2]]

cédulas = [[200, 1],
           [100, 2],
           [50, 3],
           [20, 5],
           [10, 10],
           [5, 15],
           [2, 20],
           [1, 20],
           [0.5, 30],
           [0.25, 40],
           [0.1, 50],
           [0.05, 60],
           [0.01, 80]]    

senha = 2211 #Para o modo Adm
continuar = True #Manter loop do modo adm  

# Imprime a matriz de uma forma bonita e legível 
def imprimirMatriz(matriz):
    print('='*35)
    for linha in matriz:
        print(linha)
    print('='*35)

# Faz a verificação se o produto está no estoque. Se sim devolve o produto e valor, se não, devolve produto inválido/fora de estoque
def verificarEstoque(id):
    if id >= 1 and id <= (len(produtos) - 1):
        if produtos[id][3] > 0: # Verifica se tem no estoque
            print(f'Você escolheu: {produtos[id][1]} \n Valor total: R${produtos[id][2]}')
            return True
        else:
            print('Produto fora de estoque! Escolha outro')
            return False
    elif id == 999:
        return False
    else:
        print('ID inexistente! Escolha outro')
        return False

# Verifica se: Cédula é válida e valor colocado é maior que o valor do produto | E retorna nota inserida (valorPago)
def verificarValor(id):
    valor_produto = produtos[id][2]
    inputValor = float(input('Insira o valor em notas de R$200, R$100, R$50, R$20, R$10, R$5, R$2:'))
    # Repetição até inserir valor aceitável 
    while inputValor < valor_produto or inputValor not in [200, 100, 50, 20, 10, 5, 2]:
        inputValor = float(input('Insira um valor/cédula válida em notas de R$200, R$100, R$50, R$20, R$10, R$5, R$2:'))
    produtos[id][3] -= 1 #Remove produto do estoque 
    for linha in cédulas:
        if linha[0] == inputValor:
            linha[1] += 1  # Adiciona a cédula nova no estoque de cédulas
    return inputValor

# Calcula e retorna o troco
def calcularTroco(valorProduto, valorPago, id):
    troco = round(valorPago - valorProduto, 2) # arredonda p/ 2 casas dec
    trocoCentavos = int(round(troco * 100)) # Transforma em centavos para facilitar conta 
    cédulasCentavos = [[int(c[0] * 100), c[1]] for c in cédulas] # converte as notas em cédulas para centavos (e fazer toda conta em centavos)
    
    trocoResultado = [] #Cria uma matriz com a quantidade de cada nota 
    
    for i in range(len(cédulasCentavos)):
        valor, quantidade = cédulasCentavos[i] #pega o valor e em seguida a quantidade de cada linha
        if valor <= trocoCentavos and quantidade > 0:
            numCedulas = min(trocoCentavos // valor, quantidade)
            if numCedulas > 0:
                trocoResultado.append((valor / 100, numCedulas)) #Transforma em reais dnv, coloca a quant de cédulas e adiciona a matriz para printar do jeito certo
                trocoCentavos -= valor * numCedulas 
                cédulas[i][1] -= numCedulas # Reduz as cédulas do estoque
    
    if trocoCentavos > 0: #Se sobrou troco, faltou cédulas
        print(f"Não há cédulas suficientes para dar o troco exato. Retire sua nota: {valorPago}")
        produtos[id][3] += 1 #Retorna o produto pro estoque 
        return None
    
    return trocoResultado

# Função para exibir o troco formatads
def exibirTroco(troco):
    if troco:
        print(f"Troco:")
        for valor, quantidade in troco:
            print(f"{quantidade} nota(s)/moeda(s) de R${valor:.2f}")
    else:
        print("Troco exato não pode ser dado.")

# Modo do administrador - opções de edição e saque 
def modoAdm():
    global continuar
    ação = int(input('Bem-vindo Vinicius! \nO que deseja fazer hoje? \n [1] - Adicionar um produto \n [2] - Remover produto \n [3] - Atualizar estoque \n [4] - Remover dinheiro \n [5] - Sair \n'))
    if ação == 1: # Adiciona os valores a um vetor e em seguida o vetor a matriz de produtos 
        vetor =[]
        vetor.append(len(produtos))
        vetor.append(input('Qual produto deseja adicionar:'))
        vetor.append(float(input('Qual valor do produto que deseja adicionar:')))
        vetor.append(int(input('Quantas unidades desse produto deseja adicionar:')))
        produtos.append(vetor)
        imprimirMatriz(produtos)

    elif ação == 2: #Remove a linha do indice escolhido e reordena os ids seguintes 
        produtoRemovido = int(input('Qual ID do produto que deseja remover: '))
        if produtoRemovido >= 1 and produtoRemovido <= (len(produtos) - 1):
            del produtos[produtoRemovido]
            for i in range(produtoRemovido, len(produtos)):
                produtos[i][0] -= 1
            print(f'Produto: {produtos[produtoRemovido][1]} removido com sucessso!\n')
            imprimirMatriz(produtos)
        else:
            print('Produto inexistente\n')

    elif ação == 3: # atualizar o estoque 
        idEstoque = int(input('Qual id do produto que deseja atualizar: '))
        print(f'Quantidade atual de {produtos[idEstoque][1]}: {produtos[idEstoque][3]}')
        quantidade = int(input('Quantas unidades deseja colocar: '))
        produtos[idEstoque][3] += quantidade
        print(f'Valor atualizado de {produtos[idEstoque][1]}: {produtos[idEstoque][3]}\n')

    elif ação == 4: # Atualizar ou remover dinheiro 
        adicionarRemover = int(input('Vai adicionar ou remover notas?\n [1] = Adcionar \n [2] = Remover\n'))

        if adicionarRemover == 1: # Adiciona um valor x à nota escolhida 
            notaAdicionada = int(input('Qual valor da nota que deseja adicionar: '))
            quantidadeAdicionada = int(input('Quantas notas vai adicionar: '))
            for linha in cédulas:
                if cédulas[0] == notaAdicionada:
                    cédulas[1] += quantidadeAdicionada
                    print(f'Estoque de notas: {imprimirMatriz(cédulas)}')
                else: 
                    print('Valor escolhido inválido\n')
                    break
        elif adicionarRemover == 2: # Remove o total 
            total = 0
            for linha in cédulas: 
                valor = linha[0]
                quantidade = linha[1]
                total += valor * quantidade
                linha[1] = 0
            print(f'Valor total sacado: R${total}\n')
            print(f'Estoque de notas: {imprimirMatriz(cédulas)}\n')
        else:
            print('Opção inválida\n')

    elif ação == 5: # Sair do modo ADM
        continuar = False

    else:
        print('Opção inválida. Tente novamente\n')

# Loop do programa - Deixa tudo rodando conforme os inputs do usuário
while True:
    continuar = True
    imprimirMatriz(produtos)
    id = int(input('Escolha o ID do item que deseja: '))
    
    if id == 999:
        inputSenha = int(input('Digite sua senha:'))
        if inputSenha == senha:
            while continuar:
                modoAdm()
        else:
            print('Senha inválida\n')
    
    if verificarEstoque(id): # Continua apenas se o produto existir ou estiver em estoque
        valorPago = verificarValor(id) # verificarValor valida e retorna a nota inserida
        troco = calcularTroco(produtos[id][2], valorPago, id) # recebe a matriz com os valores de cada cédula
        exibirTroco(troco) 
