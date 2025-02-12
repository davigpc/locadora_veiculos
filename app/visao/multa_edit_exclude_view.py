import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.multa_controller import MultaController
from app.visao.multa_edit_view import MultaEditView

class MultaEditExcludeView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciar Multas")
        self.geometry("800x600")
        self.criar_widgets()
        self.carregar_multas()

    def criar_widgets(self):
        # Campo de pesquisa
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Buscar por Descrição:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.carregar_multas).pack(side=tk.LEFT, padx=5)

        # Treeview para listar as multas
        self.tree = ttk.Treeview(self, columns=("ID", "Descricao", "Valor", "ID_Locacao"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descricao", text="Descrição")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("ID_Locacao", text="ID da Locação")
        self.tree.column("ID", width=50)
        self.tree.column("Descricao", width=300)
        self.tree.column("Valor", width=100)
        self.tree.column("ID_Locacao", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Editar", command=self.editar_multa).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_multa).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def carregar_multas(self):
        busca = self.search_entry.get().strip()
        multas = MultaController.obter_multas()
        self.tree.delete(*self.tree.get_children())
        for multa in multas:
            # Filtra pela descrição, se o campo de busca estiver preenchido
            if not busca or busca.lower() in multa["Descricao"].lower():
                self.tree.insert("", tk.END, values=(
                    multa["ID"],
                    multa["Descricao"],
                    multa["Valor"],
                    multa["ID_Locacao"]
                ))

    def editar_multa(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma multa para editar!")
            return

        item = self.tree.item(selecionado[0])
        multa = {
            "ID": item["values"][0],
            "Descricao": item["values"][1],
            "Valor": item["values"][2],
            "ID_Locacao": item["values"][3]
        }

        def atualizar_lista():
            self.carregar_multas()

        MultaEditView(self, multa, on_edit_success=atualizar_lista)

    def excluir_multa(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma multa para excluir!")
            return

        item = self.tree.item(selecionado[0])
        multa_id = item["values"][0]

        confirmacao = messagebox.askyesno("Confirmação", "Deseja realmente excluir esta multa?")
        if confirmacao:
            # Seguindo a mesma lógica dos demais módulos, se o método de remoção retornar None, a operação foi bem-sucedida.
            if MultaController.remover_locacoes(multa_id) is None:
                messagebox.showinfo("Sucesso", "Multa excluída com sucesso!")
                self.carregar_multas()
            else:
                messagebox.showerror("Erro", "Falha ao excluir a multa!")
