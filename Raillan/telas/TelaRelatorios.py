import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import re
from controladores.controladorAbastecimento import ControladorAbastecimento

class TelaRelatorios(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controladorAbastecimento = ControladorAbastecimento()
        self.criar_tela_relatorios()

    def criar_tela_relatorios(self): 
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)   
        
        # Top title
        title_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#CFCFCF")
        title_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(title_frame, text="Relatórios", font=("Arial", 25, "bold")).pack(side="left", padx=10)

        # Filters frame
        filters_frame = ctk.CTkFrame(main_frame)
        filters_frame.pack(fill="x", pady=10, padx=10)
        
        # Date filter
        ctk.CTkLabel(filters_frame, text="Data Início (DD/MM/AAAA):").pack(side="left", padx=5)
        self.data_inicio = ctk.CTkEntry(filters_frame)
        self.data_inicio.pack(side="left", padx=5)
        self.data_inicio.bind("<KeyRelease>", self.format_data)
        
        ctk.CTkLabel(filters_frame, text="Data Fim (DD/MM/AAAA):").pack(side="left", padx=5)
        self.data_fim = ctk.CTkEntry(filters_frame)
        self.data_fim.pack(side="left", padx=5)
        self.data_fim.bind("<KeyRelease>", self.format_data)
        
        # Funcionario filter
        ctk.CTkLabel(filters_frame, text="CPF Funcionario:").pack(side="left", padx=5)
        self.cpf_funcionario = ctk.CTkEntry(filters_frame)
        self.cpf_funcionario.pack(side="left", padx=5)
        self.cpf_funcionario.bind("<KeyRelease>", self.format_cpf)
        
        # Button to list all abastecimentos
        ctk.CTkButton(filters_frame, text="Pesquisar", command=self.pesquisar_abastecimento, font=("Arial", 15, "bold")).pack(side="left", padx=10)

        # Treeview container
        self.tree_container = ctk.CTkFrame(main_frame)
        self.tree_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Totals labels
        self.total_vendas_label = ctk.CTkLabel(main_frame, text="Total de Vendas: R$0.00", font=("Arial", 15, "bold"))
        self.total_vendas_label.pack(side="left", pady=10, padx=10)
        
        self.total_litros_label = ctk.CTkLabel(main_frame, text="Total de Litros: 0.00 L", font=("Arial", 15, "bold"))
        self.total_litros_label.pack(side="left", pady=10, padx=10)

    def criar_tabela(self, dados, cabecalhos):
        # Clear previous tree if it exists
        for widget in self.tree_container.winfo_children():
            widget.destroy()

        # Formatar dados antes de inseri-los no Treeview
        dados_formatados = self.tela_formatar_dados(dados)

        # Scrollbars
        scrollbar_x = ttk.Scrollbar(self.tree_container, orient="horizontal")
        scrollbar_y = ttk.Scrollbar(self.tree_container, orient="vertical")

        # Treeview
        self.tree = ttk.Treeview(self.tree_container, columns=cabecalhos, show="headings", height=8,
                                 xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        scrollbar_x.config(command=self.tree.xview)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Configurando as colunas
        for col in cabecalhos:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        # Inserir dados
        for i, linha in enumerate(dados_formatados):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.tag_configure(tag, background='#F5F5F5' if tag == 'evenrow' else '#E8E8E8')
            self.tree.insert("", "end", values=linha, tags=(tag,))

    def pesquisar_abastecimento(self):
        data_inicio = self.data_inicio.get()
        data_fim = self.data_fim.get()
        cpf_funcionario = self.cpf_funcionario.get()

        try:

            if cpf_funcionario and data_inicio and data_fim:
                abastecimentos = self.controladorAbastecimento.listar_abastecimentos_por_funcionario_e_periodo(
                    cpf_funcionario, self.formatar_data(data_inicio), self.formatar_data(data_fim))
                total_vendas, total_litros = self.calcular_totais(abastecimentos)
            elif data_inicio and data_fim:
                abastecimentos = self.controladorAbastecimento.listar_abastecimentos_por_periodo(
                    self.formatar_data(data_inicio), self.formatar_data(data_fim))
                total_vendas, total_litros = self.controladorAbastecimento.calcular_totais(
                    self.formatar_data(data_inicio), self.formatar_data(data_fim))
            elif cpf_funcionario:
                abastecimentos = self.controladorAbastecimento.listar_abastecimentos_por_funcionario(cpf_funcionario)
                total_vendas, total_litros = self.calcular_totais(abastecimentos)
            else:
                abastecimentos = self.controladorAbastecimento.listar_abastecimentos()
                total_vendas, total_litros = self.controladorAbastecimento.calcular_totais()
            
            if not abastecimentos:
                self.mostra_mensagem("Nenhum abastecimento encontrado para os critérios fornecidos.", tipo='info')
            
            cabecalhos = ["ID", "Data", "Hora", "Bomba", "Combustível", "Litros", "Valor"]
            self.criar_tabela(abastecimentos, cabecalhos)
            self.total_vendas_label.configure(text=f"Total de Vendas: R${total_vendas:.2f}")
            self.total_litros_label.configure(text=f"Total de Litros: {total_litros:.2f} L")
        except Exception as e:
            self.mostra_mensagem(f"Erro ao buscar abastecimentos: {e}", tipo='erro')

    def calcular_totais(self, abastecimentos):
        total_vendas = sum([abastecimento[6] * abastecimento[5] for abastecimento in abastecimentos])
        total_litros = sum([abastecimento[5] for abastecimento in abastecimentos])
        return total_vendas, total_litros

    def mostra_mensagem(self, mensagem, tipo='erro'):
        if tipo == 'erro':
            messagebox.showerror("Erro", mensagem)
        elif tipo == 'info':
            messagebox.showinfo("Informação", mensagem)

    def tela_formatar_dados(self, dados):
        dados_formatados = []
        for linha in dados:
            id_abastecimento, data, hora, bomba, combustivel, litros, preco = linha
            linha_formatada = (id_abastecimento, data, hora, bomba, combustivel, litros, preco)
            dados_formatados.append(linha_formatada)
        return dados_formatados

    def format_cpf(self, event):
        entry = event.widget
        cpf = re.sub(r'\D', '', entry.get())
        formatted_cpf = cpf
        if len(cpf) > 3:
            formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}"
        if len(cpf) > 6:
            formatted_cpf = f"{formatted_cpf}.{cpf[6:9]}"
        if len(cpf) > 9:
            formatted_cpf = f"{formatted_cpf}-{cpf[9:11]}"
        entry.delete(0, tk.END)
        entry.insert(0, formatted_cpf)

    def format_data(self, event):
        entry = event.widget
        data = re.sub(r'\D', '', entry.get())
        formatted_data = data
        if len(data) > 2:
            formatted_data = f"{data[:2]}/{data[2:4]}"
        if len(data) > 4:
            formatted_data = f"{formatted_data}/{data[4:8]}"
        entry.delete(0, tk.END)
        entry.insert(0, formatted_data)

    def formatar_data(self, data):
        dia, mes, ano = data.split('/')
        return f"{ano}-{mes}-{dia}"

    def validar_numero(self, texto):
        return texto.isdigit() or texto == ""
