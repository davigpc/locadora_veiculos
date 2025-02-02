import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.multa_controller import MultaController
from app.controle.locacao_controller import LocacaoController  # Importação do controlador de locação

class MultasView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestão de Multas")
        self.geometry("800x600")
        self.lista_locacoes = []  # Lista de locações disponíveis
        self.criar_widgets()
        self.carregar_locacoes()
        self.carregar_multas()

    def criar_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Formulário
        form_frame = ttk.LabelFrame(self.main_frame, text="Dados da Multa")
        form_frame.pack(fill=tk.X, pady=10)

        ttk.Label(form_frame, text="Descrição:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.descricao_entry = ttk.Entry(form_frame, width=40)
        self.descricao_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Valor (R$):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.valor_entry = ttk.Entry(form_frame, width=15)
        self.valor_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Combobox ID_Locacao
        ttk.Label(form_frame, text="ID da Locação:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.locacao_cb = ttk.Combobox(form_frame)
        self.locacao_cb.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.locacao_cb.bind("<KeyRelease>", self.filtrar_locacoes)


        # Botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_multa).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        # Treeview para listar as multas
        self.tree = ttk.Treeview(
            self.main_frame,
            columns=("ID", "Descrição", "Valor", "ID Locação"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Valor", text="Valor (R$)")
        self.tree.heading("ID Locação", text="ID Locação")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def carregar_locacoes(self):
        """Carrega a lista de locações disponíveis e preenche o Combobox."""
        self.lista_locacoes = [str(locacao["ID"]) for locacao in LocacaoController.listar_locacoes()]
        self.locacao_cb["values"] = self.lista_locacoes

    def filtrar_locacoes(self, event):
        """Filtra os IDs de locações conforme o usuário digita."""
        texto_digitado = self.locacao_cb.get().lower()
        if texto_digitado:
            filtrados = [loc for loc in self.lista_locacoes if texto_digitado in loc.lower()]
            self.locacao_cb["values"] = filtrados
        else:
            self.locacao_cb["values"] = self.lista_locacoes  # Restaura a lista original

    def limpar_campos(self):
        """Limpa os campos do formulário."""
        self.descricao_entry.delete(0, tk.END)
        self.valor_entry.delete(0, tk.END)
        self.locacao_cb.set("")

    def carregar_multas(self):
        """Carrega as multas na tabela."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        multas = MultaController.obter_multas()
        for multa in multas:
            self.tree.insert("", tk.END, values=(
                multa["ID"],
                multa["Descricao"],
                multa["Valor"],
                multa["ID_Locacao"]
            ))

    def salvar_multa(self):
        """Salva a multa com os dados preenchidos."""
        dados = {
            "descricao": self.descricao_entry.get(),
            "valor": self.valor_entry.get(),
            "id_locacao": self.locacao_cb.get()
        }

        if not all(dados.values()):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        if MultaController.cadastrar_multa(**dados):
            messagebox.showinfo("Sucesso", "Multa cadastrada com sucesso!")
            self.carregar_multas()
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar multa!")
