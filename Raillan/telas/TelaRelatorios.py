import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
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
        title_frame = ctk.CTkFrame(main_frame,corner_radius=15, fg_color="#CFCFCF")
        title_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(title_frame, text="Relatórios", font=("Arial", 25, "bold")).pack(side="left", padx=10)

        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkButton(buttons_frame, text="Abastecimentos", command=self.pesquisar_abastecimento, 
                      font=("Arial", 15, "bold")).pack(side="right", padx=10,pady=10)
        # Add more buttons here as needed

        # Treeview container
        self.tree_container = ctk.CTkFrame(main_frame)
        self.tree_container.pack(fill="both", expand=True, padx=10, pady=10)

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
        abastecimentos = self.controladorAbastecimento.listar_abastecimentos()
        cabecalhos = ["ID", "Data", "Hora", "Bomba", "Combustível", "Litros", "Valor"]
        self.criar_tabela(abastecimentos, cabecalhos)

    def tela_formatar_dados(self, dados):
        dados_formatados = []
        for linha in dados:
            id_abastecimento, data, hora, bomba, combustivel, litros, preco = linha
            linha_formatada = (id_abastecimento, data, hora, bomba, combustivel, litros, preco)
            dados_formatados.append(linha_formatada)
        return dados_formatados
