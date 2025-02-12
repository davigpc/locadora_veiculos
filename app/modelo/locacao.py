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
                preco_diario = veiculo[0]

            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            data_fim = datetime.strptime(data_fim, "%Y-%m-%d")

            if data_fim <= data_inicio:
                print("A data final deve ser posterior à data inicial!")
                return False

            valor_total = (data_fim - data_inicio).days * preco_diario if preco_diario else None

            sql = """
                UPDATE Locacoes 
                SET Data_Inicio = %s, Data_Fim = %s, Valor_Total = %s, ID_Cliente = %s, ID_Veiculo = %s, ID_Funcionario = %s 
                WHERE ID = %s
            """
            valores = (data_inicio, data_fim, valor_total, id_cliente, id_veiculo, id_funcionario, id_locacao)
            cursor.execute(sql, valores)
            conexao.commit()
            return True

        except Exception as e:
            print(f"Erro ao editar locação: {e}")
            return None
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

            # Verifica se a locação existe
            cursor.execute("SELECT ID FROM Locacoes WHERE ID = %s", (id_locacao,))
            if not cursor.fetchone():
                print("Locação não encontrada!")
                return False
            
            # Exclui a locação
            cursor.execute("DELETE FROM Locacoes WHERE ID = %s", (id_locacao,))
            conexao.commit()
            return True

        except Exception as e:
            print(f"Erro ao remover locação: {e}")
            return None
        finally:
            cursor.close()
            conexao.close()
            
    @staticmethod
    def obter(busca=None):
        conexao = criar_conexao()
        if not conexao:
            return []
        
        try:
            cursor = conexao.cursor(dictionary=True)

            if busca:
                sql = """
                    SELECT l.*, c.Nome AS Cliente, v.Modelo AS Veiculo, f.Nome AS Funcionario
                    FROM Locacoes l
                    LEFT JOIN Clientes c ON l.ID_Cliente = c.ID
                    LEFT JOIN Veiculos v ON l.ID_Veiculo = v.ID
                    LEFT JOIN Funcionarios f ON l.ID_Funcionario = f.ID
                    WHERE c.Nome LIKE %s OR v.Modelo LIKE %s
                """
                parametro = f"%{busca}%"
                cursor.execute(sql, (parametro, parametro))
            else:
                sql = """
                    SELECT l.*, c.Nome AS Cliente, v.Modelo AS Veiculo, f.Nome AS Funcionario
                    FROM Locacoes l
                    LEFT JOIN Clientes c ON l.ID_Cliente = c.ID
                    LEFT JOIN Veiculos v ON l.ID_Veiculo = v.ID
                    LEFT JOIN Funcionarios f ON l.ID_Funcionario = f.ID
                """
                cursor.execute(sql)

            locacoes = cursor.fetchall()
            return locacoes

        except Exception as e:
            print(f"Erro ao obter locações: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()