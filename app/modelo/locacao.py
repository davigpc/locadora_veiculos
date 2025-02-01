class Locacao:
    def __init__(self, id=None, id_cliente=None, id_veiculo=None, id_funcionario=None, data_inicio=None, data_fim=None, valor_total=None):
        self.id = id
        self.id_cliente = id_cliente
        self.id_veiculo = id_veiculo
        self.id_funcionario = id_funcionario
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.valor_total = valor_total

    def to_dict(self):
        """Converte o objeto Locacao em um dicionário."""
        return {
            "ID": self.id,
            "ID_Cliente": self.id_cliente,
            "ID_Veiculo": self.id_veiculo,
            "ID_Funcionario": self.id_funcionario,
            "Data_Inicio": self.data_inicio,
            "Data_Fim": self.data_fim,
            "Valor_Total": self.valor_total
        }

    @classmethod
    def from_dict(cls, dados):
        """Cria um objeto Locacao a partir de um dicionário."""
        return cls(
            id=dados.get("ID"),
            id_cliente=dados.get("ID_Cliente"),
            id_veiculo=dados.get("ID_Veiculo"),
            id_funcionario=dados.get("ID_Funcionario"),
            data_inicio=dados.get("Data_Inicio"),
            data_fim=dados.get("Data_Fim"),
            valor_total=dados.get("Valor_Total")
        )