import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.veiculo_controller import VeiculoController

class VeiculoEditView(tk.Toplevel):
    def __init__(self, parent, veiculo, on_edit_success):
        """
        :param parent: Janela pai.
        :param veiculo: Dicionário com os dados do veículo a ser editado.
        :param on_edit_success: Callback a ser executado após edição bem-sucedida.
        """
        super().__init__(parent)
        self.title("Editar Veículo")
        self.geometry("600x400")
        self.veiculo = veiculo 
        self.on_edit_success = on_edit_success
        self.criar_widgets()

    def criar_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        form_frame = ttk.LabelFrame(self.main_frame, text="Dados do Veículo")
        form_frame.pack(fill=tk.X, pady=10)

        ttk.Label(form_frame, text="Modelo:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.modelo_entry = ttk.Entry(form_frame, width=40)
        self.modelo_entry.grid(row=0, column=1, padx=5, pady=5)
        self.modelo_entry.insert(0, self.veiculo.get("Modelo", ""))

        ttk.Label(form_frame, text="Placa:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.placa_entry = ttk.Entry(form_frame, width=20)
        self.placa_entry.grid(row=1, column=1, padx=5, pady=5)
        self.placa_entry.insert(0, self.veiculo.get("Placa", ""))

        ttk.Label(form_frame, text="Ano:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.ano_entry = ttk.Entry(form_frame, width=10)
        self.ano_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.ano_entry.insert(0, self.veiculo.get("Ano", ""))

        ttk.Label(form_frame, text="Categoria:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.categoria_entry = ttk.Entry(form_frame, width=30)
        self.categoria_entry.grid(row=3, column=1, padx=5, pady=5)
        self.categoria_entry.insert(0, self.veiculo.get("Categoria", ""))

        ttk.Label(form_frame, text="Preço Diário:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.preco_entry = ttk.Entry(form_frame, width=15)
        self.preco_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.preco_entry.insert(0, self.veiculo.get("Preco_Diario", ""))

        # Botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_alteracoes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def salvar_alteracoes(self):
        modelo = self.modelo_entry.get()
        placa = self.placa_entry.get()
        ano = self.ano_entry.get()
        categoria = self.categoria_entry.get()
        preco_diario = self.preco_entry.get()

        if not all([modelo, placa, ano, categoria, preco_diario]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            ano = int(ano)
            preco_diario = float(preco_diario)
        except ValueError:
            messagebox.showwarning("Aviso", "Ano deve ser inteiro e Preço Diário deve ser um número!")
            return

        sucesso = VeiculoController.editar_veiculo(self.veiculo["ID"], modelo, placa, ano, categoria, preco_diario)
        if sucesso:
            messagebox.showinfo("Sucesso", "Veículo editado com sucesso!")
            self.on_edit_success()
            self.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao editar veículo!")
