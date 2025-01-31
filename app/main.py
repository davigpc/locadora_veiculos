from app.banco import criar_tabelas
from app.visao.main_view import MainView

if __name__ == "__main__":
    criar_tabelas()  # Cria as tabelas no banco de dados
    app = MainView()  # Inicia a interface gráfica
    app.mainloop()    # Executa o loop principal da interface