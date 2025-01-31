class Veiculo:
    def __init__(self, id=None, modelo=None, placa=None, ano=None, categoria=None, preco_diario=None):
        self.id = id
        self.modelo = modelo
        self.placa = placa
        self.ano = ano
        self.categoria = categoria
        self.preco_diario = preco_diario

    def to_dict(self):
        """Converte o objeto Veículo em um dicionário."""
        return {
            "ID": self.id,
            "Modelo": self.modelo,
            "Placa": self.placa,
            "Ano": self.ano,
            "Categoria": self.categoria,
            "Preco_Diario": self.preco_diario
        }

    @classmethod
    def from_dict(cls, dados):
        """Cria um objeto Veículo a partir de um dicionário."""
        return cls(
            id=dados.get("ID"),
            modelo=dados.get("Modelo"),
            placa=dados.get("Placa"),
            ano=dados.get("Ano"),
            categoria=dados.get("Categoria"),
            preco_diario=dados.get("Preco_Diario")
        )