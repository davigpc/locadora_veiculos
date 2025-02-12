import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.locacao_controller import LocacaoController
from app.visao.locacao_edit_view import LocacaoEditView  # Import atualizado

class LocacaoEditExcludeView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciar Locações")
        self.geometry("900x600")
        self.criar_widgets()
        self.carregar_locacoes()

    def criar_widgets(self):
        # Campo de pesquisa (por Nome de Cliente ou Nome do Veículo)
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Buscar por Cliente ou Veículo:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.carregar_locacoes).pack(side=tk.LEFT, padx=5)
        
        # Treeview para listar locações
        colunas = ("ID", "Cliente", "Veiculo", "Funcionario", "Data_Inicio", "Data_Fim", "Valor_Total",
                   "ID_Cliente", "ID_Veiculo", "ID_Funcionario")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings", selectmode="browse")
        
        # Definindo os headings para as colunas visíveis
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Veiculo", text="Veículo")
        self.tree.heading("Funcionario", text="Funcionário")
        self.tree.heading("Data_Inicio", text="Data Início")
        self.tree.heading("Data_Fim", text="Data Fim")
        self.tree.heading("Valor_Total", text="Valor Total")
        
        # Configura larguras para as colunas visíveis
        self.tree.column("ID", width=50)
        self.tree.column("Cliente", width=150)
        self.tree.column("Veiculo", width=150)
        self.tree.column("Funcionario", width=150)
        self.tree.column("Data_Inicio", width=100)
        self.tree.column("Data_Fim", width=100)
        self.tree.column("Valor_Total", width=100)
        
        # Oculta as colunas dos IDs dos relacionamentos
        self.tree["displaycolumns"] = ("ID", "Cliente", "Veiculo", "Funcionario", "Data_Inicio", "Data_Fim", "Valor_Total")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Botões de ações
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Editar", command=self.editar_locacao).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_locacao).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def carregar_locacoes(self):
        busca = self.search_entry.get().strip().lower()
        locacoes = LocacaoController.listar_locacoes()  # Método que retorna uma lista de dicionários com os dados da locação
        self.tree.delete(*self.tree.get_children())
        for loc in locacoes:
            # Filtra pela pesquisa: verifica se a busca está presente no nome do Cliente ou no Modelo do Veículo
            cliente = loc.get("Cliente", "").lower()
            veiculo = loc.get("Veiculo", "").lower()
            if not busca or busca in cliente or busca in veiculo:
                self.tree.insert("", tk.END, values=(
                    loc.get("ID"),
                    loc.get("Cliente"),
                    loc.get("Veiculo"),
                    loc.get("Funcionario"),
                    loc.get("Data_Inicio"),
                    loc.get("Data_Fim"),
                    loc.get("Valor_Total"),
                    loc.get("ID_Cliente"),    # Coluna oculta
                    loc.get("ID_Veiculo"),    # Coluna oculta
                    loc.get("ID_Funcionario") # Coluna oculta
                ))

    def editar_locacao(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma locação para editar!")
            return
        item = self.tree.item(selecionado[0])
        valores = item["values"]

        locacao = {
            "ID": valores[0],
            "Cliente": valores[1],
            "Veiculo": valores[2],
            "Funcionario": valores[3],
            "Data_Inicio": valores[4],
            "Data_Fim": valores[5],
            "Valor_Total": valores[6],
            "ID_Cliente": valores[7],
            "ID_Veiculo": valores[8],
            "ID_Funcionario": valores[9]
        }
        def atualizar_lista():
            self.carregar_locacoes()
        # Abre a view de edição para locação usando LocacaoEditView
        LocacaoEditView(self, locacao=locacao, on_editar_success=atualizar_lista)

    def excluir_locacao(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma locação para excluir!")
            return
        
        item = self.tree.item(selecionado[0])
        locacao_id = item["values"][0]

        confirmacao = messagebox.askyesno("Confirmação", "Deseja realmente excluir esta locação?")
        if confirmacao:
            resultado = LocacaoController.remover_locacoes(locacao_id)
            if resultado:
                messagebox.showinfo("Sucesso", "Locação excluída com sucesso!")
                self.carregar_locacoes()
            else:
                messagebox.showerror("Erro", "Falha ao excluir locação! Verifique dependências.")