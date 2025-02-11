import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.funcionario_controller import FuncionarioController
from app.visao.funcionario_view import CadastroFuncionarioView

class FuncionarioEditExcludeView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciar Funcionários")
        self.geometry("800x600")
        self.criar_widgets()
        self.carregar_funcionarios()

    def criar_widgets(self):
        # Campo de pesquisa
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Buscar por Nome ou CPF:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.carregar_funcionarios).pack(side=tk.LEFT, padx=5)

        # Lista de funcionários
        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "CPF", "Telefone"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=200)
        self.tree.column("CPF", width=100)
        self.tree.column("Telefone", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Editar", command=self.editar_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def carregar_funcionarios(self):
        busca = self.search_entry.get().strip()
        funcionarios = FuncionarioController.obter_funcionarios()
        self.tree.delete(*self.tree.get_children())
        for func in funcionarios:
            if not busca or busca.lower() in func["nome"].lower() or busca in func["cpf"]:
                self.tree.insert("", tk.END, values=(func["id"], func["nome"], func["cpf"], func["telefone"]))

    def editar_funcionario(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um funcionário para editar!")
            return
        
        item = self.tree.item(selecionado[0])
        funcionario_id = item["values"][0]

        def atualizar_lista():
            self.carregar_funcionarios()
        
        CadastroFuncionarioView(self, on_cadastro_success=atualizar_lista)

    def excluir_funcionario(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir!")
            return

        item = self.tree.item(selecionado[0])
        funcionario_cpf = item["values"][2]

        confirmacao = messagebox.askyesno("Confirmação", "Deseja realmente excluir este funcionário?")
        if confirmacao:
            if FuncionarioController.remover_funcionario(funcionario_cpf):
                messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
                self.carregar_funcionarios()
            else:
                messagebox.showerror("Erro", "Falha ao excluir funcionário!")
