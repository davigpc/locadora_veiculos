import tkinter as tk
from tkinter import ttk
from app.visao.cliente_view import ClientesView
from app.visao.veiculo_view import VeiculosView
from app.visao.locacao_view import LocacaoView
from app.visao.multa_view import MultasView
from app.visao.funcionario_view import CadastroFuncionarioView
from app.visao.funcionario_edit_exclude_view import FuncionarioEditExcludeView
from app.visao.cliente_edit_exclude_view import ClienteEditExcludeView
from app.visao.locacao_edit_exclude_view import LocacaoEditExcludeView
from app.visao.veiculo_edit_exclude_view import VeiculoEditExcludeView
from app.visao.multa_edit_exclude_view import MultaEditExcludeView 

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
        menubar = tk.Menu(self)

        # Menu Cadastros
        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menu_cadastros.add_command(label="Clientes", command=self.abrir_janela_clientes, accelerator="Ctrl+C")
        menu_cadastros.add_command(label="Veículos", command=self.abrir_janela_veiculos, accelerator="Ctrl+V")
        menu_cadastros.add_separator()
        menu_cadastros.add_command(label="Sair", command=self.destroy)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)

        # Menu Operações
        menu_operacoes = tk.Menu(menubar, tearoff=0)
        menu_operacoes.add_command(label="Nova Locação", command=self.abrir_janela_locacoes, accelerator="Ctrl+L")
        menu_operacoes.add_command(label="Cadastrar Multa", command=self.abrir_janela_multas, accelerator="Ctrl+M")
        menubar.add_cascade(label="Operações", menu=menu_operacoes)

        # Menu Edições e Exclusões
        menu_edicoes = tk.Menu(menubar, tearoff=0)
        menu_edicoes.add_command(label="Gerenciar Funcionários", command=self.abrir_janela_funcionario_ed_ex)
        menu_edicoes.add_command(label="Gerenciar Clientes", command=self.abrir_janela_clientes_ed_ex)
        menu_edicoes.add_command(label="Gerenciar Locações", command=self.abrir_janela_locacoes_ed_ex)
        menu_edicoes.add_command(label="Gerenciar Veículos", command=self.abrir_janela_veiculos_ed_ex)
        menu_edicoes.add_command(label="Gerenciar Multas", command=self.abrir_janela_multas_ed_ex)  # Nova opção
        menubar.add_cascade(label="Edições e Exclusões", menu=menu_edicoes)

        self.config(menu=menubar)

        # Atalhos do teclado
        self.bind("<Control-c>", lambda e: self.abrir_janela_clientes())
        self.bind("<Control-v>", lambda e: self.abrir_janela_veiculos())
        self.bind("<Control-l>", lambda e: self.abrir_janela_locacoes())

    def criar_area_conteudo(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.aba_dashboard = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_dashboard, text="Dashboard")
        ttk.Label(self.aba_dashboard, text="Bem-vindo ao Sistema!").pack(pady=20)

    def criar_barra_status(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
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

    def abrir_janela_multas(self):
        MultasView(self)
        self.atualizar_status("Janela de Multas aberta")

    def abrir_janela_funcionarios(self):
        CadastroFuncionarioView(self)
        self.atualizar_status("Gerenciamento de Funcionários aberto")

    def abrir_janela_funcionario_ed_ex(self):
        FuncionarioEditExcludeView(self)
        self.atualizar_status("Gerenciamento de Funcionários aberto")

    def abrir_janela_clientes_ed_ex(self):
        ClienteEditExcludeView(self)
        self.atualizar_status("Gerenciamento de Clientes aberto")

    def abrir_janela_locacoes_ed_ex(self):
        LocacaoEditExcludeView(self)
        self.atualizar_status("Gerenciamento de Locações aberto")

    def abrir_janela_veiculos_ed_ex(self):
        VeiculoEditExcludeView(self)
        self.atualizar_status("Gerenciamento de Veículos aberto")

    def abrir_janela_multas_ed_ex(self):
        MultaEditExcludeView(self)
        self.atualizar_status("Gerenciamento de Multas aberto")

if __name__ == "__main__":
    app = MainView(None)
    app.mainloop()
