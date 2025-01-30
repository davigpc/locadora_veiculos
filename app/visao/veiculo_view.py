import tkinter as tk
from tkinter import ttk, messagebox
from .controle.veiculos_controller import VeiculoController

class VeiculosView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestão de Veículos")
        self.geometry("800x600")
        self.criar_widgets()
        self.carregar_veiculos()

    def criar_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Formulário
        form_frame = ttk.LabelFrame(self.main_frame, text="Dados do Veículo")
        form_frame.pack(fill=tk.X, pady=10)

        ttk.Label(form_frame, text="Modelo:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.modelo_entry = ttk.Entry(form_frame, width=30)
        self.modelo_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Placa:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.placa_entry = ttk.Entry(form_frame, width=10)
        self.placa_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Ano:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.ano_entry = ttk.Entry(form_frame, width=6)
        self.ano_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Categoria:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.categoria_entry = ttk.Entry(form_frame, width=15)
        self.categoria_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Preço Diário:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.preco_entry = ttk.Entry(form_frame, width=10)
        self.preco_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        # Botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_veiculo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        # Lista de veículos
        self.tree = ttk.Treeview(
            self.main_frame,
            columns=("ID", "Modelo", "Placa", "Ano", "Categoria", "Preço Diário"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Modelo", text="Modelo")
        self.tree.heading("Placa", text="Placa")
        self.tree.heading("Ano", text="Ano")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Preço Diário", text="Preço Diário")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def limpar_campos(self):
        self.modelo_entry.delete(0, tk.END)
        self.placa_entry.delete(0, tk.END)
        self.ano_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)

    def carregar_veiculos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        veiculos = VeiculoController.listar_veiculos()
        for veiculo in veiculos:
            self.tree.insert("", tk.END, values=(
                veiculo["ID"],
                veiculo["Modelo"],
                veiculo["Placa"],
                veiculo["Ano"],
                veiculo["Categoria"],
                f"R$ {veiculo['Preco_Diario']:.2f}"
            ))

    def salvar_veiculo(self):
        dados = {
            "modelo": self.modelo_entry.get(),
            "placa": self.placa_entry.get(),
            "ano": self.ano_entry.get(),
            "categoria": self.categoria_entry.get(),
            "preco_diario": self.preco_entry.get()
        }

        if not all(dados.values()):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            dados["ano"] = int(dados["ano"])
            dados["preco_diario"] = float(dados["preco_diario"])
        except ValueError:
            messagebox.showerror("Erro", "Ano e Preço devem ser números válidos!")
            return

        if VeiculoController.cadastrar_veiculo(**dados):
            messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")
            self.carregar_veiculos()
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar veículo!")