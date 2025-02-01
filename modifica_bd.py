import mysql.connector

# Configurações da conexão
conn = mysql.connector.connect(
    host="localhost",   # ou o IP do servidor
    user="root",
    password="root",
    database="locadora"
)

cursor = conn.cursor()

cursor.execute("ALTER TABLE Funcionarios ADD COLUMN Senha VARCHAR(255) NOT NULL")
conn.commit()  # Confirma a alteração
print("Coluna 'Senha' adicionada com sucesso!")

cursor.execute("DESCRIBE Funcionarios")

# Exibir os detalhes da tabela
for row in cursor.fetchall():
    print(row)