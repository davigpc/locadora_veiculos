from app.banco import criar_tabelas
from app.visao.main_view import MainView
from app.visao.login_view import LoginView
from app.controle.funcionario_controller import FuncionarioController

def iniciar_aplicacao(funcionario):
    """Inicia a aplicação principal após o login."""
    app = MainView(funcionario)  # Passe os dados do funcionário para a MainView
    app.mainloop()

if __name__ == "__main__":
    criar_tabelas()  # Cria as tabelas no banco de dados

    # Sempre exibe a tela de login
    login_view = LoginView(None, on_login_success=iniciar_aplicacao)
    login_view.mainloop()