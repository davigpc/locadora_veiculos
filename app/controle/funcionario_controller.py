from app.modelo.funcionario import Funcionario
from app.banco import criar_conexao
import bcrypt 

class FuncionarioController:
    @staticmethod
    def cadastrar_funcionario(nome, cpf, senha, telefone, endereco):
        return Funcionario.criar(nome, cpf, senha, telefone, endereco)

    @staticmethod
    def obter_funcionarios():
        return Funcionario.listar()
    
    @staticmethod
    def autenticar(cpf, senha):
        """Verifica se as credenciais do funcionário estão corretas."""
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Funcionarios WHERE CPF = %s", (cpf,))
                funcionario = cursor.fetchone()

                if funcionario and bcrypt.checkpw(senha.encode('utf-8'), funcionario['Senha'].encode('utf-8')):
                    return funcionario  # Retorna os dados do funcionário se o login for bem-sucedido
                else:
                    return None  # Retorna None se o CPF ou senha estiverem incorretos
            except Exception as e:
                print(f"Erro ao autenticar funcionário: {e}")
                return None
            finally:
                cursor.close()
                conexao.close()
        return None
    
    @staticmethod
    def verificar_funcionarios_cadastrados():
        """Verifica se há funcionários cadastrados no banco de dados."""
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT COUNT(*) FROM Funcionarios")
                count = cursor.fetchone()[0]
                return count > 0  # Retorna True se houver funcionários cadastrados
            except Exception as e:
                print(f"Erro ao verificar funcionários: {e}")
                return False
            finally:
                cursor.close()
                conexao.close()
        return False