import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.cliente_controller import ClienteController
from app.visao.cliente_edit_view import ClienteEditView  # Certifique-se de que o nome do módulo/classe está correto

class ClienteEditExcludeView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciar Clientes")
        self.geometry("800x600")
        self.criar_widgets()
        self.carregar_clientes()

    def criar_widgets(self):
        # Campo de pesquisa
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Buscar por Nome ou CPF:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.carregar_clientes).pack(side=tk.LEFT, padx=5)

        # Lista de clientes
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
        ttk.Button(btn_frame, text="Editar", command=self.editar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def carregar_clientes(self):
        busca = self.search_entry.get().strip()
        clientes = ClienteController.obter_cliente()  # Certifique-se de que esse método retorna uma lista de clientes
        self.tree.delete(*self.tree.get_children())
        for cli in clientes:
            if not busca or busca.lower() in cli["Nome"].lower() or busca in cli["CPF"]:
                self.tree.insert("", tk.END, values=(cli["ID"], cli["Nome"], cli["CPF"], cli["Telefone"]))

    def editar_cliente(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return

        item = self.tree.item(selecionado[0])
        cliente = {
            "ID": item["values"][0],
            "Nome": item["values"][1],
            "CPF": item["values"][2],
            "Telefone": item["values"][3],
            # Se houver informações adicionais, como Rua, Número e Bairro,
            # você pode adicioná-las aqui ou realizar uma consulta extra ao banco.
            "Rua": "",
            "Numero": "",
            "Bairro": ""
        }

        def atualizar_lista():
            self.carregar_clientes()

        # Abre a view de edição, passando os dados do cliente e o callback para atualizar a lista
        ClienteEditView(self, cliente=cliente, on_editar_success=atualizar_lista)

    def excluir_cliente(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir!")
            return

        item = self.tree.item(selecionado[0])
        cliente_cpf = item["values"][2]

        confirmacao = messagebox.askyesno("Confirmação", "Deseja realmente excluir este cliente?")
        if confirmacao:
            if ClienteController.remover_cliente(cliente_cpf) is None:
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                self.carregar_clientes()
            else:
                messagebox.showerror("Erro", "Falha ao excluir Cliente!")
