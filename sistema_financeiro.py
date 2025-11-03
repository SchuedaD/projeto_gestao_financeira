# ================================================

# Sistema de Gestão Financeira

# ================================================

# Lista para guardar todas as transações

transacoes = []
# ================================================

# 1. FUNÇÃO - Adicionar transação a lista 

# ================================================

def adicionar_transacao(tipo,descricao,valor,data,categoria=None):
    
    if tipo not in ['receita','despesa']:
        raise ValueError("Tipo de transação inválido. Use 'receita' ou 'despesa'.")
    
    if valor <= 0:
        raise ValueError("O valor da transação deve ser positivo.")
        
    transacao = {
        'tipo': tipo,
        'descricao': descricao,
        'valor': valor,
        'data': data}
    
    if tipo == 'despesa' and categoria is not None:
            transacao['categoria'] = categoria

    
    transacoes.append(transacao)

    return transacao


# ================================================

# 2. FUNÇÃO - Listar transações existentes 

# ================================================

def listar_transacoes():
    if not transacoes:
        print("Nenhuma transação registrada. Experimente adicionar uma nova transação.")
        return
     
    print(f"\n📊 Total de transações: {len(transacoes)}")


    for i, t in enumerate(transacoes, 1):

       print(f'\n{i}. {t['tipo'].upper()}: {t['descricao']}')
       print(f'Valor: R$ {t['valor']:.2f}')
       print(f'Data: {t['data']}')
       if 'categoria' in t:
           print(f"Categoria: {t['categoria']}")

       

# ================================================

# 3. FUNÇÃO - Calcular o saldo atual 

# ================================================

def calcular_saldo():
    saldo = 0
    for t in transacoes:
        if t['tipo'] == 'receita':
            saldo+= t['valor']
        else:
            saldo-= t['valor']

    return saldo

# ================================================

# 4. FUNÇÃO - Filtrar por categoria 

# ================================================

def calcular_gastos_por_categoria():

    gastos = {}
    
    for t in transacoes:

        if t['tipo'] == 'despesa' and 'categoria' in t:
            
            categoria = t['categoria']
            valor = t['valor']

            if categoria in gastos:
                gastos[categoria] += valor
            else:
                gastos[categoria] = valor
    return gastos

# ================================================

# 5. FUNÇÃO - gerar relatório financeiro

# ================================================

def gerar_relatorio():
    # 1. Calcular saldo atual
    # 2. Calcular receitas e despesas totais
    # 3. Calcular gastos por despesa

    # 1. Exibir saldo
    saldo = calcular_saldo()
    print("Relatório financeiro:\n")

    print(f"Seu saldo é: R$ {saldo:.2f}\n ")

    print("=" * 30)

    # 2. Exibir receitas e despesas

    receita = 0 
    despesas = 0

    for t in transacoes:
        if t['tipo'] == 'receita':
            receita += t['valor']
        else:
            despesas += t['valor']

    print(f"\nSua receita total foi R$ {receita:.2f}")
    print(f"Sua despesa total foi R$ {despesas:.2f}\n")
    print("=" * 30)

    # 3. Exibir gastos por categoria

    gastos = calcular_gastos_por_categoria()
    print("\nSeus gastos por categoria são:\n")
    for chave, valor in gastos.items():
        print(f"{chave.capitalize()} - R$ {valor:.2f}\n")

# ================================================
# 6. FUNÇÃO - Salvar transações em arquivo
# ================================================

def salvar_arquivo(nome_arquivo='transacoes.txt'):
    """
    Salva todas as transações em um arquivo TXT.
    """
    
    try:
        # MISSÃO 1: Abrir arquivo em modo escrita
        # Dica: with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            
            # MISSÃO 2: Escrever cada transação como uma linha
            # Formato: tipo|descrição|valor|data|categoria
            for t in transacoes:
                
                # MISSÃO 3: Montar a linha de texto
                # Receita: "receita|Salário|5000.00|2024-10-01|"
                # Despesa: "despesa|Uber|20.00|2024-10-10|Transporte"
                
                tipo = t['tipo']
                descricao = t['descricao']
                valor = t['valor']
                data = t['data']
                categoria = t.get('categoria', '')  # Pega categoria ou '' se não tiver
                
                # Montar a linha com | separando os campos
                linha = f"{tipo}|{descricao}|{valor}|{data}|{categoria}\n"
                
                # MISSÃO 4: Escrever a linha no arquivo
                arquivo.write(linha)
        
        print(f"✅ Transações salvas em '{nome_arquivo}'!")
        
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")

# ================================================
# 7. FUNÇÃO - Carregar transações do arquivo
# ================================================

def carregar_arquivo(nome_arquivo='transacoes.txt'):
    """
    Carrega transações do arquivo TXT.
    """
    
    try:
        # MISSÃO 1: Abrir arquivo em modo leitura
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            
            # MISSÃO 2: Ler todas as linhas
            linhas = arquivo.readlines()
            
            # MISSÃO 3: Processar cada linha
            for linha in linhas:
                # Remover espaços e quebras de linha
                linha = linha.strip()
                
                # Pular linhas vazias
                if not linha:
                    continue
                
                # MISSÃO 4: Separar os campos usando split('|')
                partes = linha.split('|')
                
                # MISSÃO 5: Extrair cada campo
                tipo = partes[0]
                descricao = partes[1]
                valor = float(partes[2])  # Converter para número
                data = partes[3]
                categoria = partes[4] if partes[4] else None
                
                # MISSÃO 6: Criar a transação (sem adicionar duplicatas!)
                transacao = {
                    'tipo': tipo,
                    'descricao': descricao,
                    'valor': valor,
                    'data': data
                }
                
                if categoria:
                    transacao['categoria'] = categoria
                
                # Adicionar direto na lista (não usar adicionar_transacao)
                transacoes.append(transacao)
        
        print(f"✅ {len(linhas)} transações carregadas de '{nome_arquivo}'!")
        
    except FileNotFoundError:
        print(f"ℹ️ Arquivo '{nome_arquivo}' não encontrado. Começando com lista vazia.")
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {e}")


# ================================================
# PROGRAMA PRINCIPAL
# ================================================

def main():
    """
    Função principal - Menu interativo do sistema.
    """
    
    print("=" * 60)
    print("💰 SISTEMA DE GESTÃO FINANCEIRA PESSOAL")
    print("=" * 60)
    
    # Carregar dados salvos (se existirem)
    carregar_arquivo()
    
    while True:
        print("\n" + "=" * 60)
        print("MENU PRINCIPAL")
        print("=" * 60)
        print("1. ➕ Adicionar transação")
        print("2. 📋 Listar todas as transações")
        print("3. 💵 Ver saldo atual")
        print("4. 📊 Gerar relatório completo")
        print("5. 💾 Salvar dados")
        print("6. 🚪 Sair")
        print("=" * 60)
        
        opcao = input("\nEscolha uma opção (1-6): ").strip()
        
        if opcao == '1':
            # Adicionar transação
            print("\n➕ ADICIONAR TRANSAÇÃO")
            tipo = input("Tipo (receita/despesa): ").lower().strip()
            descricao = input("Descrição: ").strip()
            
            try:
                valor = float(input("Valor: R$ ").strip())
                data = input("Data (YYYY-MM-DD): ").strip()
                
                categoria = None
                if tipo == 'despesa':
                    categoria = input("Categoria: ").strip()
                
                adicionar_transacao(tipo, descricao, valor, data, categoria)
                
            except ValueError as e:
                print(f"❌ Erro: {e}")
        
        elif opcao == '2':
            # Listar transações
            listar_transacoes()
        
        elif opcao == '3':
            # Ver saldo
            saldo = calcular_saldo()
            print(f"\n💵 Saldo atual: R$ {saldo:.2f}")
        
        elif opcao == '4':
            # Relatório completo
            gerar_relatorio()
        
        elif opcao == '5':
            # Salvar
            salvar_arquivo()
        
        elif opcao == '6':
            # Sair
            print("\n💾 Deseja salvar antes de sair?")
            salvar = input("(s/n): ").lower().strip()
            if salvar == 's':
                salvar_arquivo()
            
            print("\n👋 Obrigado por usar o sistema! Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida! Escolha entre 1 e 6.")


# Executar o programa
if __name__ == "__main__":
    # IMPORTANTE: Limpar a lista inicial para testar do zero
    transacoes = [] 
    main()