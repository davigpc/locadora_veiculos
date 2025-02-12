import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.funcionario_controller import FuncionarioController

class CadastroFuncionarioView(tk.Toplevel):
    def __init__(self, parent, on_cadastro_success):
        super().__init__(parent)
        self.title("Cadastro de Funcionário")
        self.geometry("800x600")
        self.on_cadastro_success = on_cadastro_success
        self.criar_widgets()

    def criar_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Formulário
        form_frame = ttk.LabelFrame(self.main_frame, text="Dados do Funcionario")
        form_frame.pack(fill=tk.X, pady=10)

        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nome_entry = ttk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="CPF:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cpf_entry = ttk.Entry(form_frame, width=15)
        self.cpf_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Senha:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.senha_entry = ttk.Entry(form_frame, width=15, show="*")  
        self.senha_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Telefone:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.telefone_entry = ttk.Entry(form_frame, width=15)
        self.telefone_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Rua:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.rua_entry = ttk.Entry(form_frame, width=40)
        self.rua_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Número:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.numero_entry = ttk.Entry(form_frame, width=15)
        self.numero_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Bairro:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.bairro_entry = ttk.Entry(form_frame, width=40)
        self.bairro_entry.grid(row=6, column=1, padx=5, pady=5)

        # Botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.cadastrar_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.rua_entry.delete(0, tk.END)
        self.numero_entry.delete(0, tk.END)
        self.bairro_entry.delete(0, tk.END)
        
    def cadastrar_funcionario(self):
        dados = {
            "nome": self.nome_entry.get(),
            "cpf": self.cpf_entry.get(),
            "senha": self.senha_entry.get(),
            "telefone": self.telefone_entry.get(),
            "rua": self.rua_entry.get(),
            "numero": self.numero_entry.get(),
            "bairro": self.bairro_entry.get()
        }

        if not all(dados.values()):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        if FuncionarioController.cadastrar_funcionario(**dados):
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            self.on_cadastro_success() 
            self.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar funcionário!")
