from controladores.controladorTanqueCombustivel import ControladorTanqueCombustivel
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class TelaTanqueCombustivel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controladorTanqueCombustivel = ControladorTanqueCombustivel()
        self.selected_row = None
        self.cabecalhos = ["Nome", "Porcentagem Alerta", "Capacidade", "Combustível", "Volume Atual", "Status"]
        self.tanques = self.controladorTanqueCombustivel.listar_tanques()
        self.tela_listar_tanques()

    def tela_listar_tanques(self):
        self.clear_frame()

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=10)

        # Título alinhado à esquerda com fonte maior
        ctk.CTkLabel(top_frame, text="Lista de Tanques", font=("Arial", 25, "bold")).pack(side="left")

        # Botões alinhados à direita
        btn_frame = ctk.CTkFrame(top_frame)
        btn_frame.pack(side="right")

        btn_add = ctk.CTkButton(btn_frame, text="+", command=self.cadastrar_tanque)
        btn_add.pack(side="left", padx=5)

        self.btn_alterar = ctk.CTkButton(btn_frame, text="Alterar", command=self.alterar_tanque, state=tk.DISABLED)
        self.btn_alterar.pack(side="left", padx=5)

        self.btn_excluir = ctk.CTkButton(btn_frame, text="Excluir", command=self.excluir_tanque, state=tk.DISABLED)
        self.btn_excluir.pack(side="left", padx=5)

        # Criando a tabela responsiva com barra de rolagem horizontal
        self.criar_tabela(self.tanques, self.cabecalhos)

        # Adicionando botão de pesquisa na parte inferior direita
        btn_pesquisar = ctk.CTkButton(self, text="Pesquisar", command=self.pesquisar)
        btn_pesquisar.pack(side="bottom", anchor="se", padx=10, pady=10)

    def formatar_dados(self, dados):
        dados_formatados = []
        for linha in dados:
            linha_formatada = list(linha)  # Converta a tupla em lista para ser editável
            linha_formatada[1] = f"{linha_formatada[1]:.2f}%"  # Formate "Porcentagem Alerta"
            linha_formatada[2] = f"{linha_formatada[2]:.2f} L"  # Formate "Capacidade"
            linha_formatada[4] = f"{linha_formatada[4]:.2f} L"  # Formate "Volume Atual"
            linha_formatada[5] = f"{linha_formatada[5]:.2f}%"  # Formate "Status"
            dados_formatados.append(tuple(linha_formatada))  # Converta de volta para tupla
        return dados_formatados

    def criar_tabela(self, dados, cabecalhos):
        # Formatar dados antes de inseri-los no Treeview
        dados_formatados = self.formatar_dados(dados)

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
        self.tree.tag_configure('evenrow', background='#242424')
        self.tree.tag_configure('oddrow', background='#2D2E30')

        # Inserindo os dados na Treeview com cores alternadas
        for i, linha in enumerate(dados_formatados):
            if i % 2 == 0:
                self.tree.insert("", "end", values=linha, tags=('evenrow',))
            else:
                self.tree.insert("", "end", values=linha, tags=('oddrow',))

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_row = self.tree.item(selected_item[0], "values")
            self.btn_alterar.configure(state=tk.NORMAL)
            self.btn_excluir.configure(state=tk.NORMAL)
        else:
            self.selected_row = None
            self.btn_alterar.configure(state=tk.DISABLED)
            self.btn_excluir.configure(state=tk.DISABLED)

    def alterar_tanque(self):
        if self.selected_row:
            self.modal_alterar_tanque(self.selected_row)

    def modal_alterar_tanque(self, dados_tanque):
        self.modal = tk.Toplevel(self)
        self.modal.title("Alterar Tanque")

        # Centralizar o modal na tela principal
        self.modal.geometry("500x400")
        self.modal.transient(self)
        self.modal.grab_set()
        self.modal.update_idletasks()

        width = self.modal.winfo_width()
        height = self.modal.winfo_height()
        x = (self.modal.winfo_screenwidth() // 2) - (width // 2)
        y = (self.modal.winfo_screenheight() // 2) - (height // 2)
        self.modal.geometry(f'{width}x{height}+{x}+{y}')

        # Título alinhado à esquerda
        title_label = ctk.CTkLabel(self.modal, text="Alterar Tanque", font=("Arial", 25, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        self.labels = ["Nome", "Porcentagem Alerta", "Capacidade", "Combustível", "Volume Atual", "Status"]
        self.entries = {}

        for i, label in enumerate(self.labels):
            lbl = ctk.CTkLabel(self.modal, text=label)
            lbl.grid(row=i+1, column=0, padx=10, pady=5, sticky='e')
            entry = ctk.CTkEntry(self.modal, width=120)
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
            if i == 0:
                entry.insert(0, dados_tanque[i])
                entry.configure(state='disabled')  # Desabilitar edição do identificador
            else:
                entry.insert(0, dados_tanque[i])
            self.entries[label] = entry

        # Botão Atualizar
        update_button = ctk.CTkButton(self.modal, text="Atualizar", command=self.atualizar_tanque)
        update_button.grid(row=len(self.labels)+1, column=0, columnspan=2, pady=20)

        # Alinhar conteúdo ao centro
        for i in range(len(self.labels) + 2):
            self.modal.grid_rowconfigure(i, weight=1)
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=1)

    def atualizar_tanque(self):
        nome = self.entries["Nome"].get()
        capacidade = self.entries["Capacidade"].get().replace(' L', '')  # Remover ' L' e obter o número
        porcentagem_alerta = self.entries["Porcentagem Alerta"].get().replace('%', '')  # Remover '%' e obter o número
        combustivel = self.entries["Combustível"].get()
        volume_atual = self.entries["Volume Atual"].get().replace(' L', '')  # Remover ' L' e obter o número
        status = self.entries["Status"].get().replace('%', '')  # Remover '%' e obter o número
        identificadorTanque = self.selected_row[0]  # Ajustar o índice conforme necessário

        # Converter os valores para os tipos apropriados antes de enviar para o banco
        try:
            capacidade = float(capacidade)
            porcentagem_alerta = float(porcentagem_alerta)
            volume_atual = float(volume_atual)
            status = float(status)
        except ValueError:
            messagebox.showerror("Erro", "Erro ao converter os valores para números.", icon='error')
            return

        resultado = self.controladorTanqueCombustivel.atualizar_tanque(nome, capacidade, porcentagem_alerta, combustivel, volume_atual, status)
        if resultado:
            messagebox.showinfo("Sucesso", "Tanque atualizado com sucesso!", icon='info')
            self.modal.destroy()
            self.pesquisar()  # Atualizar a grid com os novos dados
        else:
            messagebox.showerror("Erro", "Erro ao atualizar o tanque.", icon='error')

    def excluir_tanque(self):
        if self.selected_row:
            identificadorTanque = self.selected_row[0]  # Ajustar o índice conforme necessário
            resultado = self.controladorTanqueCombustivel.remover_tanque(identificadorTanque)
            if resultado:
                messagebox.showinfo("Sucesso", "Tanque excluído com sucesso!", icon='info')
                self.pesquisar()
            else:
                messagebox.showerror("Erro", "Erro ao excluir o tanque.", icon='error')
            self.btn_alterar.configure(state=tk.DISABLED)
            self.btn_excluir.configure(state=tk.DISABLED)

    def pesquisar(self):
        # Lógica para pesquisar e carregar os dados na grid
        tanques = self.controladorTanqueCombustivel.listar_tanques()
        
        # Limpar a tabela atual
        for item in self.tree.get_children():
            self.tree.delete(item)
        dados = self.formatar_dados(tanques)
        # Inserir novos dados na tabela
        for index, row in enumerate(dados):
            self.tree.insert('', 'end', values=row, tags=('evenrow' if index % 2 == 0 else 'oddrow'))

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def menu_principal(self):
        # Implemente a lógica para voltar ao menu principal
        pass

    def cadastrar_tanque(self):
        self.modal_cadastrar_tanque()

    def modal_cadastrar_tanque(self):
        self.modal = tk.Toplevel(self)
        self.modal.title("Cadastrar Novo Tanque")

        # Centralizar o modal na tela principal
        self.modal.geometry("500x400")
        self.modal.transient(self)
        self.modal.grab_set()
        self.modal.update_idletasks()

        width = self.modal.winfo_width()
        height = self.modal.winfo_height()
        x = (self.modal.winfo_screenwidth() // 2) - (width // 2)
        y = (self.modal.winfo_screenheight() // 2) - (height // 2)
        self.modal.geometry(f'{width}x{height}+{x}+{y}')

        # Título alinhado à esquerda
        title_label = ctk.CTkLabel(self.modal, text="Cadastrar Novo Tanque", font=("Arial", 25, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        self.labels = ["Nome", "Porcentagem Alerta", "Capacidade", "Combustível", "Volume Atual", "Status"]
        self.entries = {}

        for i, label in enumerate(self.labels):
            lbl = ctk.CTkLabel(self.modal, text=label)
            lbl.grid(row=i+1, column=0, padx=10, pady=5, sticky='e')

            if label == "Combustível":
                combustiveis = self.controladorTanqueCombustivel.controladorSistema.controladorTipoCombustivel.listar_tipo_combustivel()
                self.combustivel_var = tk.StringVar()
                entry = ttk.Combobox(self.modal, textvariable=self.combustivel_var, values=combustiveis)
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
            else:
                entry = ctk.CTkEntry(self.modal, width=120)
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')

            self.entries[label] = entry

        # Botão Cadastrar
        cadastrar_button = ctk.CTkButton(self.modal, text="Cadastrar", command=self.salvar_novo_tanque)
        cadastrar_button.grid(row=len(self.labels)+1, column=0, columnspan=2, pady=20)

        # Alinhar conteúdo ao centro
        for i in range(len(self.labels) + 2):
            self.modal.grid_rowconfigure(i, weight=1)
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=1)

    def salvar_novo_tanque(self):
        nome = self.entries["Nome"].get()
        capacidade = self.entries["Capacidade"].get().replace(' L', '')  # Remover ' L' e obter o número
        porcentagem_alerta = self.entries["Porcentagem Alerta"].get().replace('%', '')  # Remover '%' e obter o número
        combustivel = self.combustivel_var.get()
        volume_atual = self.entries["Volume Atual"].get().replace(' L', '')  # Remover ' L' e obter o número
        status = self.entries["Status"].get().replace('%', '')  # Remover '%' e obter o número

        # Converter os valores para os tipos apropriados antes de enviar para o banco
        try:
            capacidade = float(capacidade)
            porcentagem_alerta = float(porcentagem_alerta)
            volume_atual = float(volume_atual)
            status = float(status)
        except ValueError:
            messagebox.showerror("Erro", "Erro ao converter os valores para números.", icon='error')
            return

        resultado = self.controladorTanqueCombustivel.adicionar_tanque(nome, capacidade, porcentagem_alerta, combustivel, volume_atual, status)
        if resultado:
            messagebox.showinfo("Sucesso", "Novo tanque cadastrado com sucesso!", icon='info')
            self.modal.destroy()
            self.pesquisar()  # Atualizar a grid com os novos dados
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar o novo tanque.", icon='error')




if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1200x800")
    app = TelaTanqueCombustivel(root)
    app.pack(fill="both", expand=True)
    root.mainloop()