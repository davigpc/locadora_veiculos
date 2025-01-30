from app.banco import criar_conexao

class Cliente:
    @staticmethod
    def criar(nome, cpf, telefone, endereco):
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """
                    INSERT INTO Clientes 
                    (Nome, CPF, Telefone, Endereco)
                    VALUES (%s, %s, %s, %s)
                """
                valores = (nome, cpf, telefone, endereco)
                cursor.execute(sql, valores)
                conexao.commit()
                return True
            except Exception as e:
                print(f"Erro ao criar cliente: {e}")
                return False
            finally:
                cursor.close()
                conexao.close()
        return False

    @staticmethod
    def listar():
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Clientes")
                clientes = cursor.fetchall()
                return clientes
            except Exception as e:
                print(f"Erro ao listar clientes: {e}")
                return []
            finally:
                cursor.close()
                conexao.close()
        return []