import mysql.connector
from mysql.connector import Error

def criar_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'
        )
        cursor = conexao.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS locadora;")
        conexao.commit()
        cursor.close()
        conexao.close()
        print("Banco de dados 'locadora' verificado/criado com sucesso.")
    except Error as err:
        print(f"Erro ao criar banco de dados: {err}")

def criar_conexao():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='locadora'
        )
        return conexao
    except Error as err:
        print(f"Erro de conexão: {err}")
        return None

def criar_tabelas():
    comandos_sql = [
        """
        CREATE TABLE IF NOT EXISTS Clientes (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            Nome VARCHAR(255) NOT NULL,
            CPF VARCHAR(11) UNIQUE NOT NULL,
            Telefone VARCHAR(15),
            Rua VARCHAR(255) DEFAULT '',
            Numero INT DEFAULT 0,
            Bairro VARCHAR(100) DEFAULT ''
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Veiculos (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            Modelo VARCHAR(255) NOT NULL,
            Placa VARCHAR(7) UNIQUE NOT NULL,
            Ano INT,
            Categoria VARCHAR(50),
            Preco_Diario DECIMAL(10,2)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Funcionarios (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            Nome VARCHAR(255) NOT NULL,
            CPF VARCHAR(11) UNIQUE NOT NULL,
            Senha VARCHAR(255) NOT NULL,
            Telefone VARCHAR(15),
            Rua VARCHAR(255),
            Numero INT,
            Bairro VARCHAR(100)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Locacoes (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            Data_Inicio DATE NOT NULL,
            Data_Fim DATE NOT NULL,
            Valor_Total DECIMAL(10,2),
            ID_Cliente INT,
            ID_Veiculo INT,
            ID_Funcionario INT,
            FOREIGN KEY (ID_Cliente) REFERENCES Clientes(ID),
            FOREIGN KEY (ID_Veiculo) REFERENCES Veiculos(ID),
            FOREIGN KEY (ID_Funcionario) REFERENCES Funcionarios(ID)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Multas (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            Descricao VARCHAR(100) NOT NULL,
            Valor DECIMAL(10,2) NOT NULL,
            ID_Locacao INT NOT NULL,
            FOREIGN KEY (ID_Locacao) REFERENCES Locacoes(ID) ON DELETE CASCADE,
            INDEX idx_id_locacao (ID_Locacao)
        )
        """
    ]

    conexao = criar_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            for comando in comandos_sql:
                cursor.execute(comando)
            conexao.commit()
            print("Tabelas criadas com sucesso!")

            # Verifica se as colunas existem antes de atualizar registros
            cursor.execute("SHOW COLUMNS FROM Clientes LIKE 'Rua';")
            if cursor.fetchone():
                cursor.execute("UPDATE Clientes SET Rua = '', Numero = 0, Bairro = '' WHERE Rua IS NULL;")
                conexao.commit()
                print("Registros atualizados com sucesso!")
        except Error as e:
            print(f"Erro ao criar tabelas ou atualizar registros: {e}")
        finally:
            cursor.close()
            conexao.close()

# Executando
criar_banco()  # Primeiro, cria o banco de dados se não existir
criar_tabelas()  # Agora, conecta ao banco e cria as tabelas
