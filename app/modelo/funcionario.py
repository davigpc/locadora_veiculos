from app.banco import criar_conexao
import bcrypt 

class Funcionario:
    @staticmethod
    def criar(nome, cpf, senha, telefone, rua, numero, bairro):
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()

                # Criptografa a senha antes de salvar no banco de dados
                senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

                sql = """
                    INSERT INTO Funcionarios 
                    (Nome, CPF, Senha, Telefone, Rua, Numero, Bairro)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                valores = (nome, cpf, senha_criptografada, telefone, rua, numero, bairro)
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
                funcionarios = cursor.fetchall()
                return funcionarios
            except Exception as e:
                print(f"Erro ao listar Funcionarios: {e}")
                return []
            finally:
                cursor.close()
                conexao.close()
        return []
    
    @staticmethod            
    def editar(id_funcionario, nome, cpf, senha, telefone, rua, numero, bairro):
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
            if rua:
                sql += "Rua = %s, "
                valores.append(rua)
            if numero:
                sql += "Numero = %s, "
                valores.append(numero)
            if bairro:
                sql += "Bairro = %s, "
                valores.append(bairro)

            sql = sql.rstrip(', ') + " WHERE ID = %s"
            valores.append(id_funcionario)
            cursor.execute(sql, valores)
            conexao.commit()
        except Exception as e:
            print(f"Erro ao editar funcionário: {e}")
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
            
    def obter(busca=None):
        conexao = criar_conexao()
        if not conexao:
            return []
        
        try:
            cursor = conexao.cursor(dictionary=True)  # Certifique-se que retorna um dicionário
            
            if busca:
                sql = "SELECT * FROM Funcionarios WHERE Nome LIKE %s OR CPF LIKE %s"
                parametro = f"%{busca}%"
                cursor.execute(sql, (parametro, parametro))
            else:
                sql = "SELECT * FROM Funcionarios"
                cursor.execute(sql)
            
            funcionarios = cursor.fetchall()

            # 🔍 Depuração: Imprime os dados retornados
            print("Funcionários retornados:", funcionarios)

            return funcionarios
        except Exception as e:
            print(f"Erro ao obter funcionários: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()
