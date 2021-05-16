import MySQLdb
from decouple import config


def conectar():
    """
    Função para conectar ao servidor
    """
    try:
        connected = MySQLdb.connect(
            db=config('db'),
            host=config('host'),
            user=config('user'),
            passwd=config('passwd')
        )
        return connected
    except MySQLdb.Error as e:
        print(f'Erro na conexão: {e}')


def desconectar(connected):
    """ 
    Função para desconectar do servidor.
    """
    if connected:
        connected.close()


def listar():
    """
    Função para listar os produtos
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    if len(produtos) > 0:
        for produto in produtos:
            print(f'ID: {produto[0]}')
            print(f'NOME: {produto[1]}')
            print(f'PREÇO {produto[2]}')
            print(f'ESTOQUE: {produto[3]}')
    else:
        print('Não existem produtos cadastrados')
    desconectar(conn)


def inserir():
    """
    Função para inserir um produto
    """
    conn = conectar()
    cursor = conn.cursor()
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe a quantidade em estoque: '))
    cursor.execute(f"INSERT INTO produtos (nome, preco, estoque) VALUES ('{nome}',{preco},{estoque})")
    conn.commit()

    if cursor.rowcount == 1:
        print(f'O produto {nome} foi inserido com sucesso.\nPreço: {preco}\nQuantidade: {estoque}')
    else:
        print(f'Não foi possivel inserir o produto {nome}')
    desconectar(conn)

def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()
    cursor = conn.cursor()
    codigo = int(input('Digite o codigo do produto a ser atualizado'))
    nome = input('Novo nome do produto: ')
    preco = float(input('Novo preço do produto: '))
    estoque = int(input('Nova quantidade em estoque'))
    cursor.execute(f"UPDATE produtos SET nome='{nome}', preco={preco}, estoque={estoque} WHERE id={codigo}")
    conn.commit()
    if cursor.rowcount == 1:
        print(f'Produto: {nome} foi atualizado')
    else:
        print(f'Erro ao atualizar o produto {nome}')
    desconectar(conn)

def deletar():
    """
    Função para deletar um produto
    """
    print('Deletando produto...')


def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
