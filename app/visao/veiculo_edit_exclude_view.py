import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.veiculo_controller import VeiculoController
from app.visao.veiculo_edit_view import VeiculoEditView 

class VeiculoEditExcludeView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciar Veículos")
        self.geometry("800x600")
        self.criar_widgets()
        self.carregar_veiculos()

    def criar_widgets(self):
   
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Buscar por Modelo ou Placa:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.carregar_veiculos).pack(side=tk.LEFT, padx=5)

        # Treeview para listar os veículos
        self.tree = ttk.Treeview(self, columns=("ID", "Modelo", "Placa", "Ano", "Categoria", "Preco_Diario"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Modelo", text="Modelo")
        self.tree.heading("Placa", text="Placa")
        self.tree.heading("Ano", text="Ano")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Preco_Diario", text="Preço Diário")
        self.tree.column("ID", width=50)
        self.tree.column("Modelo", width=200)
        self.tree.column("Placa", width=100)
        self.tree.column("Ano", width=50)
        self.tree.column("Categoria", width=100)
        self.tree.column("Preco_Diario", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Botões de ações
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Editar", command=self.editar_veiculo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_veiculo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def carregar_veiculos(self):
        """
        Carrega (ou recarrega) a lista de veículos filtrando pelo campo de busca.
        """
        busca = self.search_entry.get().strip()
        veiculos = VeiculoController.obter_veiculo(busca)
        # Limpa a Treeview
        self.tree.delete(*self.tree.get_children())
        for veic in veiculos:
            self.tree.insert("", tk.END, values=(
                veic["ID"],
                veic["Modelo"],
                veic["Placa"],
                veic["Ano"],
                veic["Categoria"],
                veic["Preco_Diario"]
            ))

    def editar_veiculo(self):
        """
        Abre a view de edição para o veículo selecionado.
        """
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo para editar!")
            return
        item = self.tree.item(selecionado[0])
        veiculo = {
            "ID": item["values"][0],
            "Modelo": item["values"][1],
            "Placa": item["values"][2],
            "Ano": item["values"][3],
            "Categoria": item["values"][4],
            "Preco_Diario": item["values"][5],
        }

        def atualizar_lista():
            self.carregar_veiculos()

        VeiculoEditView(self, veiculo, on_edit_success=atualizar_lista)

    def excluir_veiculo(self):
        """
        Exclui o veículo selecionado, após confirmação do usuário.
        """
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo para excluir!")
            return
        item = self.tree.item(selecionado[0])
        veiculo_id = item["values"][0]
        confirmacao = messagebox.askyesno("Confirmação", "Deseja realmente excluir este veículo?")
        if confirmacao:
            sucesso = VeiculoController.remover_veiculo(veiculo_id)
            if sucesso:
                messagebox.showinfo("Sucesso", "Veículo excluído com sucesso!")
                self.carregar_veiculos()
            else:
                messagebox.showerror("Erro", "Falha ao excluir veículo!")
