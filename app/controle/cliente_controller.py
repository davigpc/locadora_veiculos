from app.modelo.cliente import Cliente

class ClienteController:
    @staticmethod
    def cadastrar_cliente(nome, cpf, telefone, endereco):
        return Cliente.criar(nome, cpf, telefone, endereco)

    @staticmethod
    def obter_clientes():
        return Cliente.listar()
    
    @staticmethod            
    def editar_cliente(id_funcionario, nome, cpf, senha, telefone, endereco):
        return Cliente.editar(id_funcionario, nome, cpf, senha, telefone, endereco)
    
    @staticmethod
    def remover_cliente(cpf_cliente):
        return Cliente.remover(cpf_cliente)
