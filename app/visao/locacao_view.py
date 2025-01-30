import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.controle.locacao_controller import LocacaoController
from app.controle.cliente_controller import ClienteController
from app.controle.veiculo_controller import VeiculoController

class LocacaoView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestão de Locações")
        self.geometry("1000x800")
        self.criar_widgets()
        self.carregar_locacoes()

    def criar_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Formulário
        form_frame = ttk.LabelFrame(self.main_frame, text="Nova Locação")
        form_frame.pack(fill=tk.X, pady=10)

        # Combobox Cliente
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cliente_cb = ttk.Combobox(form_frame, state="readonly")
        self.cliente_cb.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.atualizar_clientes()

        # Combobox Veículo
        ttk.Label(form_frame, text="Veículo:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.veiculo_cb = ttk.Combobox(form_frame, state="readonly")
        self.veiculo_cb.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.atualizar_veiculos()

        # Datas
        ttk.Label(form_frame, text="Data Início:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_inicio = ttk.Entry(form_frame)
        self.data_inicio.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.data_inicio.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(form_frame, text="Data Fim:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_fim = ttk.Entry(form_frame)
        self.data_fim.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        # Botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Calcular Valor", command=self.calcular_valor).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar Locação", command=self.salvar_locacao).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        # Lista de locações
        self.tree = ttk.Treeview(
            self.main_frame,
            columns=("ID", "Cliente", "Veículo", "Início", "Fim", "Valor"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Veículo", text="Veículo")
        self.tree.heading("Início", text="Início")
        self.tree.heading("Fim", text="Fim")
        self.tree.heading("Valor", text="Valor (R$)")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def atualizar_clientes(self):
        """Carrega os clientes no Combobox."""
        clientes = ClienteController.obter_clientes()
        self.cliente_cb["values"] = [f"{c['ID']} - {c['Nome']}" for c in clientes]

    def atualizar_veiculos(self):
        """Carrega os veículos no Combobox."""
        veiculos = VeiculoController.listar_veiculos()
        self.veiculo_cb["values"] = [f"{v['ID']} - {v['Modelo']} ({v['Placa']})" for v in veiculos]

    def calcular_valor(self):
        """Calcula o valor total da locação com base no preço diário e no período."""
        try:
            veiculo_id = int(self.veiculo_cb.get().split(" - ")[0])
            veiculo = VeiculoController.buscar_veiculo(veiculo_id)
            preco_diario = veiculo["Preco_Diario"]

            data_inicio = datetime.strptime(self.data_inicio.get(), "%d/%m/%Y")
            data_fim = datetime.strptime(self.data_fim.get(), "%d/%m/%Y")
            dias = (data_fim - data_inicio).days

            if dias < 1:
                messagebox.showerror("Erro", "Data final deve ser posterior à data inicial!")
                return

            valor_total = dias * preco_diario
            messagebox.showinfo("Cálculo", f"Valor Total: R$ {valor_total:.2f}")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha no cálculo: {str(e)}")

    def carregar_locacoes(self):
        """Carrega as locações na Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        locacoes = LocacaoController.listar_locacoes()
        for loc in locacoes:
            self.tree.insert("", tk.END, values=(
                loc["ID"],
                loc["Cliente"],
                loc["Veiculo"],
                loc["Data_Inicio"],
                loc["Data_Fim"],
                f"R$ {loc['Valor_Total']:.2f}"
            ))

    def salvar_locacao(self):
        """Salva uma nova locação no banco de dados."""
        try:
            cliente_id = int(self.cliente_cb.get().split(" - ")[0])
            veiculo_id = int(self.veiculo_cb.get().split(" - ")[0])
            data_inicio = datetime.strptime(self.data_inicio.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            data_fim = datetime.strptime(self.data_fim.get(), "%d/%m/%Y").strftime("%Y-%m-%d")

            if LocacaoController.cadastrar_locacao(
                id_cliente=cliente_id,
                id_veiculo=veiculo_id,
                data_inicio=data_inicio,
                data_fim=data_fim
            ):
                messagebox.showinfo("Sucesso", "Locação registrada com sucesso!")
                self.carregar_locacoes()
            else:
                messagebox.showerror("Erro", "Falha ao registrar locação!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar locação: {str(e)}")