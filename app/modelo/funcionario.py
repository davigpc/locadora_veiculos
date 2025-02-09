from app.banco import criar_conexao
import bcrypt 

class Funcionario:
    @staticmethod
    def criar(nome, cpf, senha, telefone, endereco):
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()

                # Criptografa a senha antes de salvar no banco de dados
                senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

                sql = """
                    INSERT INTO Funcionarios 
                    (Nome, CPF, Senha, Telefone, Endereco)
                    VALUES (%s, %s, %s, %s, %s)
                """
                valores = (nome, cpf, senha_criptografada, telefone, endereco)
                cursor.execute(sql, valores)
                conexao.commit()
                return True
            except Exception as e:
                print(f"Erro ao criar Funcionario: {e}")
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
                cursor.execute("SELECT * FROM Funcionarios")
                Funcionarios = cursor.fetchall()
                return Funcionarios
            except Exception as e:
                print(f"Erro ao listar Funcionarios: {e}")
                return []
            finally:
                cursor.close()
                conexao.close()
        return []
    
    @staticmethod            
    def editar(id_funcionario, nome, cpf, senha, telefone, endereco):
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            valores = []
            sql = "UPDATE Funcionarios SET "
            
            if nome:
                sql += "Nome = %s, "
                valores.append(nome)
            if cpf:
                sql += "CPF = %s, "
                valores.append(cpf)
            if senha:
                sql += "Senha = %s, "
                valores.append(senha)
            if telefone:
                sql += "Telefone = %s, "
                valores.append(telefone)
            if endereco:
                sql += "Endereco = %s, "
                valores.append(endereco)
            sql = sql.rstrip(', ') + " WHERE ID = %s"
            valores.append(id_funcionario)
            cursor.execute(sql, valores)
            conexao.commit()
        except Exception as e:
            print(f"Erro ao editar veículo: {e}")
        finally:
            cursor.close()
            conexao.close()     
    
    @staticmethod
    def remover(cpf_funcionario):
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            sql = "DELETE FROM Funcionarios WHERE CPF = %s"
            cursor.execute(sql, (cpf_funcionario,))
            conexao.commit()
        except Exception as e:
            print(f"Erro ao remover funcionario: {e}")
            return None
        finally:
            cursor.close()
            conexao.close() 
    
    