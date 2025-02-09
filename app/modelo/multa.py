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
    
    @staticmethod            
    def editar(id_multa, descricao, valor, id_locacao):
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            valores = []
            sql = "UPDATE Multas SET "
            
            if descricao:
                sql += "Descricao = %s, "
                valores.append(descricao)
            if valor:
                sql += "Valor = %s, "
                valores.append(valor)
            if id_locacao:
                sql += "ID_Locacao = %s, "
                valores.append(id_locacao)
            sql = sql.rstrip(', ') + " WHERE ID = %s"
            valores.append(id_multa)
            cursor.execute(sql, valores)
            conexao.commit()
        except Exception as e:
            print(f"Erro ao editar multa: {e}")
        finally:
            cursor.close()
            conexao.close()   
    
    @staticmethod
    def remover(id_multa):
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            sql = "DELETE FROM Multas WHERE ID = %s"
            cursor.execute(sql, (id_multa,))
            conexao.commit()
        except Exception as e:
            print(f"Erro ao remover multa: {e}")
            return None
        finally:
            cursor.close()
            conexao.close()    