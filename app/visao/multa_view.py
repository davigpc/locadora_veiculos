import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.multa_controler import MultaController

class MultasView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestão de Multas")
        self.geometry("800x600")
        self.criar_widgets()
        self.carregar_Multas()

    def criar_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Formulário
        form_frame = ttk.LabelFrame(self.main_frame, text="Dados da Multa")
        form_frame.pack(fill=tk.X, pady=10)

        ttk.Label(form_frame, text="Descricao:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.descricao_entry = ttk.Entry(form_frame, width=40)
        self.descricao_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Valor:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.valor_entry = ttk.Entry(form_frame, width=15)
        self.valor_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Combobox ID_Locacao (Filtro dinâmico)
        ttk.Label(form_frame, text="Locação:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.veiculo_cb = ttk.Combobox(form_frame)
        self.veiculo_cb.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.veiculo_cb.bind("<KeyRelease>", self.filtrar_locacoes)

        # Botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_Multa).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def carregar_veiculos(self):
        """Carrega a lista de veículos do banco e preenche o Combobox."""
        self.lista_veiculos = [f"{v['ID']} - {v['Modelo']} ({v['Placa']})" for v in VeiculoController.listar_veiculos()]
        self.veiculo_cb["values"] = self.lista_veiculos

    def filtrar_veiculos(self, event):
        """Filtra os veículos conforme o usuário digita."""
        texto_digitado = self.veiculo_cb.get().lower()
        if texto_digitado:
            filtrados = [v for v in self.lista_veiculos if texto_digitado in v.lower()]
            self.veiculo_cb["values"] = filtrados
        else:
            self.veiculo_cb["values"] = self.lista_veiculos  # Restaura todos os valores

    def limpar_campos(self):
        self.descricao_entry.delete(0, tk.END)
        self.valor_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.endereco_entry.delete(0, tk.END)

    def carregar_Multas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        Multas = MultaController.obter_Multas()
        for Multa in Multas:
            self.tree.insert("", tk.END, values=(
                Multa["ID"],
                Multa["descricao"],
                Multa["valor"],
                Multa["Telefone"],
                Multa["Endereco"]
            ))

    def salvar_Multa(self):
        dados = {
            "descricao": self.descricao_entry.get(),
            "valor": self.valor_entry.get(),
            "telefone": self.telefone_entry.get(),
            "endereco": self.endereco_entry.get()
        }

        if not all(dados.values()):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        if MultaController.cadastrar_Multa(**dados):
            messagebox.showinfo("Sucesso", "Multa cadastrado com sucesso!")
            self.carregar_Multas()
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar Multa!")