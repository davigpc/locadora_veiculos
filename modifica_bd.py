import mysql.connector 

# Configurações da conexão
conn = mysql.connector.connect(
    host="localhost",  
    user="root",
    password="root",
    database="locadora"
)

cursor = conn.cursor()

# Verifica se as colunas já existem antes de tentar adicionar
try:
    cursor.execute("SHOW COLUMNS FROM Clientes LIKE 'Rua'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE Clientes ADD COLUMN Rua VARCHAR(255)")
        print("Coluna 'Rua' adicionada com sucesso!")

    cursor.execute("SHOW COLUMNS FROM Clientes LIKE 'Numero'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE Clientes ADD COLUMN Numero INT")
        print("Coluna 'Numero' adicionada com sucesso!")

    cursor.execute("SHOW COLUMNS FROM Clientes LIKE 'Bairro'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE Clientes ADD COLUMN Bairro VARCHAR(100)")
        print("Coluna 'Bairro' adicionada com sucesso!")

    # Adicionando colunas para a tabela Funcionarios (sem alterar Clientes)
    cursor.execute("SHOW COLUMNS FROM Funcionarios LIKE 'Rua'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE Funcionarios ADD COLUMN Rua VARCHAR(255)")
        print("Coluna 'Rua' adicionada à tabela 'Funcionarios' com sucesso!")

    cursor.execute("SHOW COLUMNS FROM Funcionarios LIKE 'Numero'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE Funcionarios ADD COLUMN Numero INT")
        print("Coluna 'Numero' adicionada à tabela 'Funcionarios' com sucesso!")

    cursor.execute("SHOW COLUMNS FROM Funcionarios LIKE 'Bairro'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE Funcionarios ADD COLUMN Bairro VARCHAR(100)")
        print("Coluna 'Bairro' adicionada à tabela 'Funcionarios' com sucesso!")

    conn.commit()
except mysql.connector.Error as err:
    print(f"Erro ao adicionar colunas: {err}")

# Exibe a estrutura da tabela para confirmar
cursor.execute("DESCRIBE Clientes")
for row in cursor.fetchall():
    print(row)

cursor.execute("DESCRIBE Funcionarios")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
