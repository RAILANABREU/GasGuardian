from controladores.controladorPosto import ControladorPosto
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



class TelaPosto(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.controlador = ControladorPosto()
        self.selected_row = None
        self.cabecalhos = ["Nome do Posto", "CNPJ", "Chave PIX"]
        self.criar_tela_posto()

    def mostra_mensagem(self, mensagem, tipo='erro'):
        if tipo == 'erro':
            messagebox.showerror("Erro", mensagem)
        elif tipo == 'info':
            messagebox.showinfo("Informação", mensagem)

    def criar_tela_posto(self):
        self.clear_frame()

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", pady=20, padx=20)     

        title_frame = ctk.CTkFrame(top_frame, corner_radius=15, fg_color="#CFCFCF")
        title_frame.pack(side="left", padx=10, pady=10)   
        
        ctk.CTkLabel(title_frame, text="Gerenciamento de Postos", font=("Arial", 25, "bold")).pack(side="left")

        btn_frame = ctk.CTkFrame(top_frame)
        btn_frame.pack(side="right")

        btn_add = ctk.CTkButton(btn_frame, text="+", command=self.modal_cadastrar_posto)
        btn_add.pack(side="left", padx=1)

        self.btn_alterar = ctk.CTkButton(btn_frame, text="Alterar", command=self.tela_alterar_posto, state=tk.DISABLED)
        self.btn_alterar.pack(side="left", padx=1)

        try:
            posto = self.controlador.listar_posto()
            if not posto:
                self.mostra_mensagem("Nenhum posto cadastrado.", 'info')
                return
        except Exception as e:
            self.mostra_mensagem(f"Erro ao listar postos: {e}", 'erro')

        self.criar_tabela(posto, self.cabecalhos)

    def criar_tabela(self, dados, cabecalhos):
        # Formatar dados antes de inseri-los no Treeview

        # Frame container para Treeview e Scrollbar com espaçamento
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=10, pady=20)

        # Adicionando Scrollbars
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal")
        scrollbar_y = ttk.Scrollbar(container, orient="vertical")

        self.tree = ttk.Treeview(container, columns=cabecalhos, show="headings", height=8,
                                xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x.config(command=self.tree.xview)
        scrollbar_y.config(command=self.tree.yview)

        self.tree.pack(side="left", fill="both", expand=True)

        # Adicionando evento de seleção de linha
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Configurando as colunas
        for col in cabecalhos:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        # Configurando as tags para cores alternadas
        self.tree.tag_configure('evenrow', background='#F5F5F5')
        self.tree.tag_configure('oddrow', background='#E8E8E8')

        # Inserindo os dados na Treeview com cores alternadas
        for i, linha in enumerate(dados):
            if i % 2 == 0:
                self.tree.insert("", "end", values=linha, tags=('evenrow',))
            else:
                self.tree.insert("", "end", values=linha, tags=('oddrow',))

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_row = self.tree.item(selected_item[0], "values")
            self.btn_alterar.configure(state=tk.NORMAL)
        else:
            self.selected_row = None
            self.btn_alterar.configure(state=tk.DISABLED)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def modal_cadastrar_posto(self):
        self.modal = tk.Toplevel(self)
        self.modal.title("Cadastrar Novo Posto")
        self.centralize_modal(self.modal, 500, 400)

        ctk.CTkLabel(self.modal, text="Cadastrar Novo Posto", font=("Arial", 16, "bold")).pack(pady=20)

        fields = ["Nome do Posto", "CNPJ", "Chave PIX"]
        entries = {}
        for i, field in enumerate(fields):
            ctk.CTkLabel(self.modal, text=field).pack()
            entry = ctk.CTkEntry(self.modal, width=250)
            entry.pack(pady=10)
            entries[field] = entry

        ctk.CTkButton(self.modal, text="Salvar", command=lambda: self.salvar_posto(entries)).pack(pady=20)

    def salvar_posto(self, entries):
        nome = entries["Nome do Posto"].get().strip()
        cnpj = entries["CNPJ"].get().strip()
        chave_pix = entries["Chave PIX"].get().strip()
        if not nome or not cnpj or not chave_pix:
            self.mostra_mensagem("Todos os campos devem ser preenchidos!", 'erro')
            return
        try:
            self.controlador.adicionar_posto(nome, cnpj, chave_pix)
            self.mostra_mensagem("Posto cadastrado com sucesso!", 'info')
            self.modal.destroy()
            self.pesquisar()
        except Exception as e:
            self.mostra_mensagem(f"Erro ao cadastrar posto: {e}", 'erro')

    def centralize_modal(self, modal, width, height):
        modal.geometry(f"{width}x{height}+{(modal.winfo_screenwidth()//2) - (width//2)}+{(modal.winfo_screenheight()//2) - (height//2)}")

    def tela_alterar_posto(self):
        if not self.selected_row:
            self.mostra_mensagem("Selecione um posto na lista para alterar!", 'info')
            return

        self.modal = tk.Toplevel(self)
        self.modal.title("Alterar Posto")
        self.centralize_modal(self.modal, 500, 400)

        ctk.CTkLabel(self.modal, text="Alterar Posto", font=("Arial", 16, "bold")).pack(pady=20)

        fields = ["Nome do Posto", "CNPJ", "Chave PIX"]
        entries = {}
        for i, field in enumerate(fields):
            ctk.CTkLabel(self.modal, text=field).pack()
            entry = ctk.CTkEntry(self.modal, width=250)
            entry.insert(0, self.selected_row[i])  # Load existing data
            entry.pack(pady=10)
            entries[field] = entry

        ctk.CTkButton(self.modal, text="Salvar Alterações", command=lambda: self.salvar_alteracoes_posto(entries)).pack(pady=20)

    def salvar_alteracoes_posto(self, entries):
        nome = entries["Nome do Posto"].get().strip()
        cnpj = entries["CNPJ"].get().strip()
        chave_pix = entries["Chave PIX"].get().strip()
        if not nome or not cnpj or not chave_pix:
            self.mostra_mensagem("Todos os campos devem ser preenchidos!", 'erro')
            return
        try:
            self.controlador.atualizar_posto(cnpj, nome, chave_pix)
            self.mostra_mensagem("Posto atualizado com sucesso!", 'info')
            self.modal.destroy()
            self.pesquisar()
        except Exception as e:
            self.mostra_mensagem(f"Erro ao atualizar posto: {e}", 'erro')

    def pesquisar(self):
        # Lógica para pesquisar e carregar os dados na grid
        try:
            posto = self.controlador.listar_posto()
        except Exception as e:
            self.mostra_mensagem(f"Erro ao pesquisar os tanques: {e}", tipo='erro')
            return
        # Limpar a tabela atual
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Inserir novos dados na tabela
        for index, row in enumerate(posto):
            self.tree.insert('', 'end', values=row, tags=('evenrow' if index % 2 == 0 else 'oddrow'))