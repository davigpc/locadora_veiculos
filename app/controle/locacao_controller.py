from app.modelo.locacao import Locacao
from app.banco import criar_conexao

class LocacaoController:
    @staticmethod
    def cadastrar_locacao(id_cliente, id_veiculo, data_inicio, data_fim):
        """Cadastra uma nova locação no banco de dados."""
        conexao = criar_conexao()
        if not conexao:
            return False

        try:
            cursor = conexao.cursor()
            sql = """
                INSERT INTO Locacoes 
                (ID_Cliente, ID_Veiculo, Data_Inicio, Data_Fim)
                VALUES (%s, %s, %s, %s)
            """
            valores = (id_cliente, id_veiculo, data_inicio, data_fim)
            cursor.execute(sql, valores)
            conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao cadastrar locação: {e}")
            return False
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def listar_locacoes():
        """Retorna todas as locações cadastradas."""
        conexao = criar_conexao()
        if not conexao:
            return []

        try:
            cursor = conexao.cursor(dictionary=True)
            sql = """
                SELECT 
                    Locacoes.ID,
                    Clientes.Nome AS Cliente,
                    Veiculos.Modelo AS Veiculo,
                    Locacoes.Data_Inicio,
                    Locacoes.Data_Fim,
                    Locacoes.Valor_Total
                FROM Locacoes
                INNER JOIN Clientes ON Locacoes.ID_Cliente = Clientes.ID
                INNER JOIN Veiculos ON Locacoes.ID_Veiculo = Veiculos.ID
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar locações: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()