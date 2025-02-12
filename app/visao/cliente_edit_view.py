import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.cliente_controller import ClienteController

class ClienteEditView(tk.Toplevel):
    def __init__(self, parent, cliente=None, on_editar_success=None):
        """
        Cria a view para editar um cliente.
        
        :param parent: Janela pai.
        :param cliente: Dicionário com os dados do cliente.
        :param on_editar_success: Callback para atualizar a lista após a edição.
        """
        super().__init__(parent)
        self.title("Editar Cliente")
        self.geometry("800x600")
        self.on_editar_success = on_editar_success
        self.cliente = cliente
        self.criar_widgets()
        if self.cliente:
            self.preencher_campos()

    def criar_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Formulário (altere o título do frame para "Dados do Cliente")
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

        ttk.Label(form_frame, text="Rua:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.rua_entry = ttk.Entry(form_frame, width=40)
        self.rua_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Número:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.numero_entry = ttk.Entry(form_frame, width=15)
        self.numero_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Bairro:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.bairro_entry = ttk.Entry(form_frame, width=40)
        self.bairro_entry.grid(row=5, column=1, padx=5, pady=5)

        # Botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.editar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def preencher_campos(self):
        """Preenche os campos com os dados do cliente e trava o CPF."""
        self.nome_entry.insert(0, self.cliente.get("Nome", ""))
        self.cpf_entry.insert(0, self.cliente.get("CPF", ""))
        self.cpf_entry.config(state="disabled")  # CPF não poderá ser editado
        self.telefone_entry.insert(0, self.cliente.get("Telefone", ""))
        self.rua_entry.insert(0, self.cliente.get("Rua", ""))
        self.numero_entry.insert(0, str(self.cliente.get("Numero", "")))
        self.bairro_entry.insert(0, self.cliente.get("Bairro", ""))

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        # O campo CPF permanece travado e não é limpo
        self.telefone_entry.delete(0, tk.END)
        self.rua_entry.delete(0, tk.END)
        self.numero_entry.delete(0, tk.END)
        self.bairro_entry.delete(0, tk.END)
        
    def editar_cliente(self):
        nome = self.nome_entry.get().strip()
        cpf = self.cpf_entry.get().strip()  # Valor obtido do campo travado
        telefone = self.telefone_entry.get().strip()
        rua = self.rua_entry.get().strip()
        numero = self.numero_entry.get().strip()
        bairro = self.bairro_entry.get().strip()

        if not nome or not cpf:
            messagebox.showerror("Erro", "Nome e CPF são obrigatórios.")
            return
        
        try:
            numero = int(numero)
        except ValueError:
            numero = 0

        cliente_id = self.cliente.get("ID")
        resultado = ClienteController.editar_cliente(
            cliente_id, nome, cpf, telefone, rua, numero, bairro
        )

        if resultado is None:
            messagebox.showerror("Erro", "Falha ao editar cliente!")
        else:
            messagebox.showinfo("Sucesso", "Cliente editado com sucesso!")
            if self.on_editar_success:
                self.on_editar_success()
            self.destroy()
