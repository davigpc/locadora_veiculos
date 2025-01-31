import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.cliente_controller import ClienteController

class ClientesView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestão de Clientes")
        self.geometry("800x600")
        self.criar_widgets()
        self.carregar_clientes()

    def criar_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Formulário
        form_frame = ttk.LabelFrame(self.main_frame, text="Dados do Cliente")
        form_frame.pack(fill=tk.X, pady=10)

        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nome_entry = ttk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="CPF:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cpf_entry = ttk.Entry(form_frame, width=15)
        self.cpf_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Telefone:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.telefone_entry = ttk.Entry(form_frame, width=15)
        self.telefone_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Endereço:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.endereco_entry = ttk.Entry(form_frame, width=40)
        self.endereco_entry.grid(row=3, column=1, padx=5, pady=5)

        # Botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        # Lista de clientes
        self.tree = ttk.Treeview(
            self.main_frame,
            columns=("ID", "Nome", "CPF", "Telefone", "Endereço"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.endereco_entry.delete(0, tk.END)

    def carregar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        clientes = ClienteController.obter_clientes()
        for cliente in clientes:
            self.tree.insert("", tk.END, values=(
                cliente["ID"],
                cliente["Nome"],
                cliente["CPF"],
                cliente["Telefone"],
                cliente["Endereco"]
            ))

    def salvar_cliente(self):
        dados = {
            "nome": self.nome_entry.get(),
            "cpf": self.cpf_entry.get(),
            "telefone": self.telefone_entry.get(),
            "endereco": self.endereco_entry.get()
        }

        if not all(dados.values()):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        if ClienteController.cadastrar_cliente(**dados):
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.carregar_clientes()
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar cliente!")