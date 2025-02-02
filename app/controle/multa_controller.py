from app.modelo.multa import Multa

class MultaController:
    @staticmethod
    def cadastrar_multa(descricao, valor, id_locacao):
        return Multa.criar(descricao, valor, id_locacao)

    @staticmethod
    def obter_multas():
        return Multa.listar()