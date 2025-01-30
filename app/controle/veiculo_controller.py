from app.modelo.veiculo import Veiculo
from app.banco import criar_conexao

class VeiculoController:
    @staticmethod
    def cadastrar_veiculo(modelo, placa, ano, categoria, preco_diario):
        """Cadastra um novo veículo no banco de dados."""
        conexao = criar_conexao()
        if not conexao:
            return False

        try:
            cursor = conexao.cursor()
            sql = """
                INSERT INTO Veiculos 
                (Modelo, Placa, Ano, Categoria, Preco_Diario)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (modelo, placa, ano, categoria, preco_diario)
            cursor.execute(sql, valores)
            conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao cadastrar veículo: {e}")
            return False
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def listar_veiculos():
        """Retorna todos os veículos cadastrados."""
        conexao = criar_conexao()
        if not conexao:
            return []

        try:
            cursor = conexao.cursor(dictionary=True)
            sql = "SELECT * FROM Veiculos"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar veículos: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def buscar_veiculo(id_veiculo):
        """Busca um veículo pelo ID."""
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor(dictionary=True)
            sql = "SELECT * FROM Veiculos WHERE ID = %s"
            cursor.execute(sql, (id_veiculo,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar veículo: {e}")
            return None
        finally:
            cursor.close()
            conexao.close()