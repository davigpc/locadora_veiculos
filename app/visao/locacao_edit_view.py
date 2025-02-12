import tkinter as tk
from tkinter import ttk, messagebox
from app.controle.locacao_controller import LocacaoController
from datetime import datetime

class LocacaoEditView(tk.Toplevel):
    def __init__(self, parent, locacao=None, on_editar_success=None):
        """
        Cria a view para editar uma locação.
        
        :param parent: Janela pai.
        :param locacao: Dicionário com os dados da locação (incluindo os IDs dos relacionamentos).
        :param on_editar_success: Callback para atualizar a lista após a edição.
        """
        super().__init__(parent)
        self.title("Editar Locação")
        self.geometry("600x400")
        self.on_editar_success = on_editar_success
        self.locacao = locacao
        self.criar_widgets()
        if self.locacao:
            self.preencher_campos()

    def criar_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Frame para os dados da locação
        form_frame = ttk.LabelFrame(self.main_frame, text="Dados da Locação")
        form_frame.pack(fill=tk.X, pady=10)

        # Cliente (apenas para visualização)
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cliente_entry = ttk.Entry(form_frame, width=40)
        self.cliente_entry.grid(row=0, column=1, padx=5, pady=5)
        self.cliente_entry.config(state="disabled")

        # Veículo (apenas para visualização)
        ttk.Label(form_frame, text="Veículo:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.veiculo_entry = ttk.Entry(form_frame, width=40)
        self.veiculo_entry.grid(row=1, column=1, padx=5, pady=5)
        self.veiculo_entry.config(state="disabled")

        # Funcionário (apenas para visualização)
        ttk.Label(form_frame, text="Funcionário:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.funcionario_entry = ttk.Entry(form_frame, width=40)
        self.funcionario_entry.grid(row=2, column=1, padx=5, pady=5)
        self.funcionario_entry.config(state="disabled")

        # Data Início
        ttk.Label(form_frame, text="Data Início (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_inicio_entry = ttk.Entry(form_frame, width=20)
        self.data_inicio_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        # Data Fim
        ttk.Label(form_frame, text="Data Fim (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_fim_entry = ttk.Entry(form_frame, width=20)
        self.data_fim_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        # Botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.editar_locacao).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def preencher_campos(self):
        """Preenche os campos com os dados da locação e exibe os dados não editáveis."""
        # Preenche e trava os campos de visualização
        self.cliente_entry.config(state="normal")
        self.cliente_entry.insert(0, self.locacao.get("Cliente", ""))
        self.cliente_entry.config(state="disabled")

        self.veiculo_entry.config(state="normal")
        self.veiculo_entry.insert(0, self.locacao.get("Veiculo", ""))
        self.veiculo_entry.config(state="disabled")

        self.funcionario_entry.config(state="normal")
        self.funcionario_entry.insert(0, self.locacao.get("Funcionario", ""))
        self.funcionario_entry.config(state="disabled")

        self.data_inicio_entry.insert(0, self.locacao.get("Data_Inicio", ""))
        self.data_fim_entry.insert(0, self.locacao.get("Data_Fim", ""))

    def editar_locacao(self):
        data_inicio = self.data_inicio_entry.get().strip()
        data_fim = self.data_fim_entry.get().strip()

        if not data_inicio or not data_fim:
            messagebox.showerror("Erro", "As datas de início e fim são obrigatórias.")
            return

        try:
            # Validação do formato das datas
            datetime.strptime(data_inicio, "%Y-%m-%d")
            datetime.strptime(data_fim, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Utilize YYYY-MM-DD.")
            return

        # Obtém os IDs necessários para a edição (armazenados no dicionário recebido)
        id_locacao = self.locacao.get("ID")
        id_cliente = self.locacao.get("ID_Cliente")
        id_veiculo = self.locacao.get("ID_Veiculo")
        id_funcionario = self.locacao.get("ID_Funcionario")

        # Chama o método de edição da locação no controlador
        resultado = LocacaoController.editar_locacoes(id_locacao, id_cliente, id_veiculo, id_funcionario, data_inicio, data_fim)
        if resultado is None:
            messagebox.showerror("Erro", "Falha ao editar locação!")
        else:
            messagebox.showinfo("Sucesso", "Locação editada com sucesso!")
            if self.on_editar_success:
                self.on_editar_success()
            self.destroy()
