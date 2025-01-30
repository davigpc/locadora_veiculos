from app.modelo.cliente import Cliente

class ClienteController:
    @staticmethod
    def cadastrar_cliente(nome, cpf, telefone, endereco):
        return Cliente.criar(nome, cpf, telefone, endereco)

    @staticmethod
    def obter_clientes():
        return Cliente.listar()