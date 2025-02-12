import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.multa_controller import MultaController

class MultaEditView(tk.Toplevel):
    def __init__(self, parent, multa, on_edit_success):
        """
        :param parent: Janela pai.
        :param multa: Dicionário com os dados da multa (chaves: "ID", "Descricao", "Valor", "ID_Locacao").
        :param on_edit_success: Função callback para atualizar a lista após a edição.
        """
        super().__init__(parent)
        self.title("Editar Multa")
        self.geometry("500x300")
        self.multa = multa
        self.on_edit_success = on_edit_success
        self.criar_widgets()

    def criar_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Campo Descrição
        ttk.Label(self.main_frame, text="Descrição:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.descricao_entry = ttk.Entry(self.main_frame, width=50)
        self.descricao_entry.grid(row=0, column=1, pady=5)
        self.descricao_entry.insert(0, self.multa.get("Descricao", ""))

        # Campo Valor
        ttk.Label(self.main_frame, text="Valor:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.valor_entry = ttk.Entry(self.main_frame, width=20)
        self.valor_entry.grid(row=1, column=1, pady=5)
        self.valor_entry.insert(0, self.multa.get("Valor", ""))

        # Campo ID da Locação
        ttk.Label(self.main_frame, text="ID da Locação:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.id_locacao_entry = ttk.Entry(self.main_frame, width=20)
        self.id_locacao_entry.grid(row=2, column=1, pady=5)
        self.id_locacao_entry.insert(0, self.multa.get("ID_Locacao", ""))

        # Botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_alteracoes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def salvar_alteracoes(self):
        descricao = self.descricao_entry.get().strip()
        valor = self.valor_entry.get().strip()
        id_locacao = self.id_locacao_entry.get().strip()

        if not descricao or not valor or not id_locacao:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            valor = float(valor)
            id_locacao = int(id_locacao)
        except ValueError:
            messagebox.showwarning("Aviso", "Valor deve ser numérico e ID da Locação deve ser um número inteiro!")
            return

        sucesso = MultaController.editar_multa(self.multa["ID"], descricao, valor, id_locacao)
        if sucesso:
            messagebox.showinfo("Sucesso", "Multa editada com sucesso!")
            self.on_edit_success()
            self.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao editar a multa!")
