import tkinter as tk
from tkinter import ttk
from app.visao.cliente_view import ClientesView
from app.visao.veiculo_view import VeiculosView
from app.visao.locacao_view import LocacaoView


class MainView(tk.Tk):
    def __init__(self, funcionario):
        super().__init__()
        self.title("Sistema de Locação de Veículos - v1.0")
        self.geometry("1024x768")
        self.configure(bg="#f0f0f0")

        self.criar_menu_principal()
        self.criar_area_conteudo()
        self.criar_barra_status()

    def criar_menu_principal(self):
        # Configuração do menu superior
        menubar = tk.Menu(self)

        # Menu Cadastros
        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menu_cadastros.add_command(
            label="Clientes",
            command=self.abrir_janela_clientes,
            accelerator="Ctrl+C"
        )
        menu_cadastros.add_command(
            label="Veículos",
            command=self.abrir_janela_veiculos,
            accelerator="Ctrl+V"
        )
        menu_cadastros.add_separator()
        menu_cadastros.add_command(label="Sair", command=self.destroy)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)

        # Menu Operações
        menu_operacoes = tk.Menu(menubar, tearoff=0)
        menu_operacoes.add_command(
            label="Nova Locação",
            command=self.abrir_janela_locacoes,
            accelerator="Ctrl+L"
        )
        menubar.add_cascade(label="Operações", menu=menu_operacoes)

        self.config(menu=menubar)

        # Atalhos do teclado
        self.bind("<Control-c>", lambda e: self.abrir_janela_clientes())
        self.bind("<Control-v>", lambda e: self.abrir_janela_veiculos())
        self.bind("<Control-l>", lambda e: self.abrir_janela_locacoes())

    def criar_area_conteudo(self):
        # Área principal com abas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aba Dashboard
        self.aba_dashboard = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_dashboard, text="Dashboard")

        # Widgets da aba dashboard (exemplo)
        ttk.Label(self.aba_dashboard, text="Bem-vindo ao Sistema!").pack(pady=20)

    def criar_barra_status(self):
        # Barra de status inferior
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")

        self.status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def atualizar_status(self, mensagem):
        self.status_var.set(mensagem)

    def abrir_janela_clientes(self):
        ClientesView(self)
        self.atualizar_status("Janela de Clientes aberta")

    def abrir_janela_veiculos(self):
        VeiculosView(self)
        self.atualizar_status("Janela de Veículos aberta")

    def abrir_janela_locacoes(self):
        LocacaoView(self)
        self.atualizar_status("Janela de Locações aberta")


if __name__ == "__main__":
    app = MainView()
    app.mainloop()