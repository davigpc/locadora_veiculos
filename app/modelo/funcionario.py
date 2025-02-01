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
    
    