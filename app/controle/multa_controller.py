from app.modelo.multa import Multa

class MultaController:
    @staticmethod
    def cadastrar_multa(descricao, valor, id_locacao):
        return Multa.criar(descricao, valor, id_locacao)

    @staticmethod
    def obter_multas():
        return Multa.listar()
    
    @staticmethod            
    def editar_multa(id_multa, descricao, valor, id_locacao):
        return Multa.editar(id_multa, descricao, valor, id_locacao)
    
    @staticmethod  
    def remover_locacoes(id_multa):
        return Multa.remover(id_multa)