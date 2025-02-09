from app.banco import criar_conexao
from datetime import datetime  


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
        
    @staticmethod            
    def editar(id_locacao, id_cliente, id_veiculo, id_funcionario, data_inicio, data_fim):
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            
            preco_diario = None
            if id_veiculo:
                cursor.execute("SELECT Preco_Diario FROM Veiculos WHERE ID = %s", (id_veiculo,))
                veiculo = cursor.fetchone()
                if not veiculo:
                    print("Veículo não encontrado!")
                    return False
                preco_diario = veiculo[0]  # Preço diário do veículo

            # Converte as datas de strings para objetos datetime
            if data_inicio:
                data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            if data_fim:
                data_fim = datetime.strptime(data_fim, "%Y-%m-%d")

            # Calcula o valor total se ambas as datas forem fornecidas
            valor_total = None
            if data_inicio and data_fim:
                dias = (data_fim - data_inicio).days
                if dias < 1:
                    print("A data final deve ser posterior à data inicial!")
                    return False
                if preco_diario:
                    valor_total = dias * preco_diario

            valores = []
            sql = "UPDATE Locacoes SET "

            if data_inicio:
                sql += "Data_Inicio = %s, "
                valores.append(data_inicio)
            if data_fim:
                sql += "Data_Fim = %s, "
                valores.append(data_fim)
            if valor_total is not None:
                sql += "Valor_Total = %s, "
                valores.append(valor_total)
            if id_cliente:
                sql += "ID_Cliente = %s, "
                valores.append(id_cliente)
            if id_veiculo:
                sql += "ID_Veiculo = %s, "
                valores.append(id_veiculo)
            if id_funcionario:
                sql += "ID_Funcionario = %s, "
                valores.append(id_funcionario)
                sql = sql.rstrip(', ') + " WHERE ID = %s"
                valores.append(id_locacao)
                cursor.execute(sql, valores)
                conexao.commit()
        except Exception as e:
            print(f"Erro ao editar locação: {e}")
        finally:
            cursor.close()
            conexao.close()
        
    @staticmethod
    def remover(id_locacao):
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            sql = "DELETE FROM Locacoes WHERE ID = %s"
            cursor.execute(sql, (id_locacao,))
            conexao.commit()
        except Exception as e:
            print(f"Erro ao remover locação: {e}")
            return None
        finally:
            cursor.close()
            conexao.close() 