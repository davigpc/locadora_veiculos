from app.banco import criar_conexao

class Multa:
    @staticmethod
    def criar(descricao, valor, id_locacao):
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()

                sql = """
                    INSERT INTO Multas 
                    (Descricao, Valor, ID_Locacao)
                    VALUES (%s, %s, %s)
                """
                valores = (descricao, valor, id_locacao)
                cursor.execute(sql, valores)
                conexao.commit()
                return True
            except Exception as e:
                print(f"Erro ao criar Multa: {e}")
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
                cursor.execute("SELECT * FROM Multas")
                Multas = cursor.fetchall()
                return Multas
            except Exception as e:
                print(f"Erro ao listar Multas: {e}")
                return []
            finally:
                cursor.close()
                conexao.close()
        return []
    
    