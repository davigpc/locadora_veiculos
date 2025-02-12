from app.banco import criar_conexao

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

    @staticmethod
    def editar(id_veiculo, modelo, placa, ano, categoria, preco_diario):
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            valores = []
            sql = "UPDATE Veiculos SET "
            
            if modelo:
                sql += "Modelo = %s, "
                valores.append(modelo)
            if placa:
                sql += "Placa = %s, "
                valores.append(placa)
            if ano:
                sql += "Ano = %s, "
                valores.append(ano)
            if categoria:
                sql += "Categoria = %s, "
                valores.append(categoria)
            if preco_diario:
                sql += "Preco_Diario = %s, "
                valores.append(preco_diario)
                
            sql = sql.rstrip(', ') + " WHERE ID = %s"
            valores.append(id_veiculo)
            cursor.execute(sql, valores)
            conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao editar veículo: {e}")
            return False
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def remover(id_veiculo):
        conexao = criar_conexao()
        if not conexao:
            return None

        try:
            cursor = conexao.cursor()
            sql = "DELETE FROM Veiculos WHERE ID = %s"
            cursor.execute(sql, (id_veiculo,))
            conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover veículo: {e}")
            return False
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def obter(busca=None):
        """
        Retorna uma lista de veículos. Se o parâmetro 'busca' for informado,
        filtra pelos campos Modelo ou Placa.
        """
        conexao = criar_conexao()
        if not conexao:
            return []
        
        try:
            cursor = conexao.cursor(dictionary=True)
            if busca:
                sql = "SELECT * FROM Veiculos WHERE Modelo LIKE %s OR Placa LIKE %s"
                parametro = f"%{busca}%"
                cursor.execute(sql, (parametro, parametro))
            else:
                sql = "SELECT * FROM Veiculos"
                cursor.execute(sql)
            
            veiculos = cursor.fetchall()
            print("Veículos retornados:", veiculos)
            return veiculos
        except Exception as e:
            print(f"Erro ao obter veículos: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()
