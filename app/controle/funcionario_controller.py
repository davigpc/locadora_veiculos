from app.modelo.funcionario import Funcionario
from app.banco import criar_conexao
import bcrypt 

class FuncionarioController:

    @staticmethod
    def listar_funcionarios():
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
                    return funcionario 
                else:
                    return None 
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
                return count > 0 
            except Exception as e:
                print(f"Erro ao verificar funcionários: {e}")
                return False
            finally:
                cursor.close()
                conexao.close()
        return False
    
    @staticmethod
    def remover_funcionario(cpf_funcionario):
        return Funcionario.remover(cpf_funcionario)
    
    @staticmethod
    def cadastrar_funcionario(nome, cpf, senha, telefone, rua, numero, bairro):
        return Funcionario.criar(nome, cpf, senha, telefone, rua, numero, bairro)

    @staticmethod
    def editar_funcionario(id_funcionario, nome, cpf, senha, telefone, rua, numero, bairro):
        return Funcionario.editar(id_funcionario, nome, cpf, senha, telefone, rua, numero, bairro)
    def obter_funcionarios(busca=None):
        return Funcionario.obter(busca)