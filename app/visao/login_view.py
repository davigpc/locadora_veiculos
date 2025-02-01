import tkinter as tk
from tkinter import ttk, messagebox
from app.visao.funcionario_view import CadastroFuncionarioView
from app.controle.funcionario_controller import FuncionarioController
from app.modelo.funcionarioLogado import FuncionarioLogado

class LoginView(tk.Toplevel):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.title("Login")
        self.geometry("300x200")
        self.on_login_success = on_login_success
        self.criar_widgets()

    def criar_widgets(self):
        ttk.Label(self, text="CPF:").grid(row=0, column=0, padx=10, pady=10)
        self.cpf_entry = ttk.Entry(self)
        self.cpf_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
        self.senha_entry = ttk.Entry(self, show="*")
        self.senha_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self, text="Login", command=self.realizar_login).grid(row=2, column=0, columnspan=2, pady=10)

        # Botão "Cadastrar" para abrir a tela de cadastro de funcionários
        ttk.Button(self, text="Cadastrar", command=self.abrir_cadastro).grid(row=3, column=0, columnspan=2, pady=10)

    def realizar_login(self):
        cpf = self.cpf_entry.get()
        senha = self.senha_entry.get()

        funcionario = FuncionarioController.autenticar(cpf, senha)
        if funcionario:
            funcionario_logado = FuncionarioLogado()
            funcionario_logado.set_funcionario(funcionario)
            self.on_login_success(funcionario)
            self.destroy()
        else:
            messagebox.showerror("Erro", "CPF ou senha incorretos!")

    def abrir_cadastro(self):
        """Abre a tela de cadastro de funcionários."""
        cadastro_view = CadastroFuncionarioView(
            self,  # Passa a tela de login como parent
            on_cadastro_success=lambda: messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
        )
        cadastro_view.grab_set()  # Mantém o foco na tela de cadastro