import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.controle.locacao_controller import LocacaoController
from app.controle.cliente_controller import ClienteController
from app.controle.veiculo_controller import VeiculoController
from app.modelo.funcionarioLogado import FuncionarioLogado

class LocacaoView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestão de Locações")
        self.geometry("1000x800")
        
        self.lista_clientes = []  # Lista completa de clientes
        self.lista_veiculos = []  # Lista completa de veículos
        
        self.criar_widgets()
        self.carregar_clientes()
        self.carregar_veiculos()

    def criar_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Formulário
        form_frame = ttk.LabelFrame(self.main_frame, text="Nova Locação")
        form_frame.pack(fill=tk.X, pady=10)

        # Combobox Cliente (Filtro dinâmico)
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cliente_cb = ttk.Combobox(form_frame)
        self.cliente_cb.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.cliente_cb.bind("<KeyRelease>", self.filtrar_clientes)

        # Combobox Veículo (Filtro dinâmico)
        ttk.Label(form_frame, text="Veículo:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.veiculo_cb = ttk.Combobox(form_frame)
        self.veiculo_cb.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.veiculo_cb.bind("<KeyRelease>", self.filtrar_veiculos)

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
            columns=("ID", "Cliente", "Veículo", "Início", "Fim", "Valor", "Funcionario"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Veículo", text="Veículo")
        self.tree.heading("Início", text="Início")
        self.tree.heading("Fim", text="Fim")
        self.tree.heading("Valor", text="Valor (R$)")
        self.tree.heading("Funcionario", text="Funcionario")
        self.tree.pack(fill=tk.BOTH, expand=True)


    def carregar_clientes(self):
        """Carrega a lista de clientes do banco e preenche o Combobox."""
        self.lista_clientes = [f"{c['ID']} - {c['Nome']}" for c in ClienteController.obter_clientes()]
        self.cliente_cb["values"] = self.lista_clientes

    def carregar_veiculos(self):
        """Carrega a lista de veículos do banco e preenche o Combobox."""
        self.lista_veiculos = [f"{v['ID']} - {v['Modelo']} ({v['Placa']})" for v in VeiculoController.listar_veiculos()]
        self.veiculo_cb["values"] = self.lista_veiculos

    def filtrar_clientes(self, event):
        """Filtra os clientes conforme o usuário digita."""
        texto_digitado = self.cliente_cb.get().lower()
        if texto_digitado:
            filtrados = [c for c in self.lista_clientes if texto_digitado in c.lower()]
            self.cliente_cb["values"] = filtrados
        else:
            self.cliente_cb["values"] = self.lista_clientes 

    def filtrar_veiculos(self, event):
        """Filtra os veículos conforme o usuário digita."""
        texto_digitado = self.veiculo_cb.get().lower()
        if texto_digitado:
            filtrados = [v for v in self.lista_veiculos if texto_digitado in v.lower()]
            self.veiculo_cb["values"] = filtrados
        else:
            self.veiculo_cb["values"] = self.lista_veiculos 

    def calcular_valor(self):
        """Calcula o valor total da locação com base no preço diário e no período."""
        try:
            veiculo_id = int(self.veiculo_cb.get().split(" - ")[0])
            veiculo = VeiculoController.buscar_veiculo(veiculo_id)
            preco_diario = veiculo["Preco_Diario"]

            if preco_diario is None:
                messagebox.showerror("Erro", "Preço diário do veículo não está definido!")
                return

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
       
            valor_total = loc['Valor_Total'] if loc['Valor_Total'] is not None else 0.00
            id_funcionario = FuncionarioLogado().get_id()
            self.tree.insert("", tk.END, values=(
                loc["ID"],
                loc["Cliente"],
                loc["Veiculo"],
                loc["Data_Inicio"],
                loc["Data_Fim"],
                f"R$ {valor_total:.2f}",
                f"{id_funcionario}"
            ))

    def salvar_locacao(self):
        """Salva uma nova locação no banco de dados."""
        try:
            cliente_selecionado = self.cliente_cb.get()
            veiculo_selecionado = self.veiculo_cb.get()

            if not cliente_selecionado or not veiculo_selecionado:
                messagebox.showerror("Erro", "Selecione um cliente e um veículo!")
                return
            
            try:
                data_inicio = datetime.strptime(self.data_inicio.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
                data_fim = datetime.strptime(self.data_fim.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido! Use o formato DD/MM/AAAA.")
                return

            cliente_id = int(cliente_selecionado.split(" - ")[0])
            veiculo_id = int(veiculo_selecionado.split(" - ")[0])
            data_inicio = datetime.strptime(self.data_inicio.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            data_fim = datetime.strptime(self.data_fim.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            funcionario_id = FuncionarioLogado().get_id()

            if LocacaoController.veiculo_ja_alugado(veiculo_id, data_inicio, data_fim):
                messagebox.showerror("Erro", "Este veículo já está alugado nesse período!")
                return  

            if LocacaoController.cadastrar_locacao(
                id_cliente=cliente_id,
                id_veiculo=veiculo_id,
                id_funcionario=funcionario_id,
                data_inicio=data_inicio,
                data_fim=data_fim
            ):
                messagebox.showinfo("Sucesso", "Locação registrada com sucesso!")
                self.carregar_locacoes()
            else:
                messagebox.showerror("Erro", "Falha ao registrar locação!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar locação: {str(e)}")