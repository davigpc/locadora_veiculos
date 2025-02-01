import mysql.connector
from mysql.connector import Error


def criar_conexao():
    try:
        # Primeiro conecta sem especificar o banco
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',  # seu usuário
            password='root'
        )
        cursor = conexao.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS locadora")
        conexao.commit()
        conexao.close()

        # Agora conecta ao banco específico
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
            Endereco VARCHAR(255)
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
            Endereco VARCHAR(255)
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
        CREATE TABLE IF NOT EXISTS Pagamentos (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            Data_Pagamento DATE NOT NULL,
            Valor_Pago DECIMAL(10,2) NOT NULL,
            ID_Locacao INT,
            FOREIGN KEY (ID_Locacao) REFERENCES Locacoes(ID)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Multas (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            Descricao VARCHAR(255) NOT NULL,
            Valor DECIMAL(10,2) NOT NULL,
            ID_Locacao INT,
            FOREIGN KEY (ID_Locacao) REFERENCES Locacoes(ID)
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
        except Error as err:
            print(f"Erro ao criar tabelas: {err}")
        finally:
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    criar_tabelas()