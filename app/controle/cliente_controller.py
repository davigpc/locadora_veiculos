from app.modelo.cliente import Cliente

class ClienteController:
    @staticmethod
    def cadastrar_cliente(nome, cpf, telefone, rua, numero, bairro):
        return Cliente.criar(nome, cpf, telefone, rua, numero, bairro)

    @staticmethod
    def obter_clientes():
        return Cliente.listar()
    
    @staticmethod            
    def editar_cliente(id_cliente, nome, cpf, telefone, rua, numero, bairro):
        return Cliente.editar(id_cliente, nome, cpf, telefone, rua, numero, bairro)
    
    @staticmethod
    def remover_cliente(cpf_cliente):
        return Cliente.remover(cpf_cliente)
    def obter_cliente(busca = None):
        return Cliente.obter(busca)