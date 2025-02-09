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
    
    @staticmethod            
    def editar(id_cliente, nome, cpf, telefone, endereco):
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            valores = []
            sql = "UPDATE Clientes SET "
            
            if nome:
                sql += "Nome = %s, "
                valores.append(nome)
            if cpf:
                sql += "CPF = %s, "
                valores.append(cpf)
            if telefone:
                sql += "Telefone = %s, "
                valores.append(telefone)
            if endereco:
                sql += "Endereco = %s, "
                valores.append(endereco)
            sql = sql.rstrip(', ') + " WHERE ID = %s"
            valores.append(id_cliente)
            cursor.execute(sql, valores)
            conexao.commit()
        except Exception as e:
            print(f"Erro ao editar veículo: {e}")
        finally:
            cursor.close()
            conexao.close() 
    
    @staticmethod
    def remover(cpf_cliente):
        
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            sql = "DELETE FROM Clientes WHERE CPF = %s"
            cursor.execute(sql, (cpf_cliente,))
            conexao.commit()
        except Exception as e:
            print(f"Erro ao remover cliente: {e}")
            return None
        finally:
            cursor.close()
            conexao.close() 