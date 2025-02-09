from app.modelo.locacao import Locacao
from app.banco import criar_conexao
from datetime import datetime  

class LocacaoController:
    @staticmethod
    def cadastrar_locacao(id_cliente, id_veiculo, id_funcionario, data_inicio, data_fim):
        """Cadastra uma nova locação no banco de dados."""
        conexao = criar_conexao()
        if not conexao:
            return False

        try:
            cursor = conexao.cursor()

            # Busca o preço diário do veículo
            cursor.execute("SELECT Preco_Diario FROM Veiculos WHERE ID = %s", (id_veiculo,))
            veiculo = cursor.fetchone()
            if not veiculo:
                print("Veículo não encontrado!")
                return False

            preco_diario = veiculo[0]  # Preço diário do veículo

            # Converte as datas de strings para objetos datetime
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            data_fim = datetime.strptime(data_fim, "%Y-%m-%d")

            # Calcula o número de dias da locação
            dias = (data_fim - data_inicio).days
            if dias < 1:
                print("A data final deve ser posterior à data inicial!")
                return False

            # Calcula o valor total da locação
            valor_total = dias * preco_diario

            # Insere a locação com o valor total calculado
            sql = """
                INSERT INTO Locacoes 
                (ID_Cliente, ID_Veiculo, ID_Funcionario, Data_Inicio, Data_Fim, Valor_Total)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (id_cliente, id_veiculo, id_funcionario, data_inicio.strftime("%Y-%m-%d"), data_fim.strftime("%Y-%m-%d"), valor_total)
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
                    Funcionarios.Nome AS Funcionario,
                    Locacoes.Data_Inicio,
                    Locacoes.Data_Fim,
                    Locacoes.Valor_Total
                FROM Locacoes
                INNER JOIN Clientes ON Locacoes.ID_Cliente = Clientes.ID
                INNER JOIN Veiculos ON Locacoes.ID_Veiculo = Veiculos.ID
                INNER JOIN Funcionarios ON Locacoes.ID_Funcionario = Funcionarios.ID
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar locações: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()



    @staticmethod
    def veiculo_ja_alugado(id_veiculo, data_inicio, data_fim):
        """Verifica se o veículo já está alugado no período selecionado."""
        conexao = criar_conexao()
        if not conexao:
            return False

        try:
            cursor = conexao.cursor()

            # Busca locações para o veículo no período selecionado
            sql = """
                SELECT COUNT(*) FROM Locacoes
                WHERE ID_Veiculo = %s
                AND (
                    (Data_Inicio BETWEEN %s AND %s) OR
                    (Data_Fim BETWEEN %s AND %s) OR
                    (%s BETWEEN Data_Inicio AND Data_Fim) OR
                    (%s BETWEEN Data_Inicio AND Data_Fim)
                )
            """
            valores = (id_veiculo, data_inicio, data_fim, data_inicio, data_fim, data_inicio, data_fim)
            cursor.execute(sql, valores)
            resultado = cursor.fetchone()

            return resultado[0] > 0  # Retorna True se houver pelo menos um conflito

        except Exception as e:
            print(f"Erro ao verificar disponibilidade do veículo: {e}")
            return False
        finally:
            cursor.close()
            conexao.close()
            
    @staticmethod  
    def editar_locacoes(id_locacao):
        return Locacao.editar(id_locacao)
    @staticmethod  
    def remover_locacoes(id_locacao, id_cliente, id_veiculo, id_funcionario, data_inicio, data_fim):
        return Locacao.remover(id_locacao, id_cliente, id_veiculo, id_funcionario, data_inicio, data_fim)