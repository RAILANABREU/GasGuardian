from controladores.controladorBombaCombustivel import ControladorBombaCombustivel
from controladores.controladorTipoCombustivel import ControladorTipoCombustivel
from controladores.controladorTanqueCombustivel import ControladorTanqueCombustivel
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def Mostra_mensagem(mensagem, tipo='erro'):
    if tipo == 'erro':
        messagebox.showerror("Erro", mensagem, icon='error')
    elif tipo == 'info':
        messagebox.showinfo("Informação", mensagem, icon='info')


class TelaBombaCombustivel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controladorBombaCombustivel = ControladorBombaCombustivel()
        self.controladorTipoCombustivel = ControladorTipoCombustivel()
        self.controladorTanqueCombustivel = ControladorTanqueCombustivel()
        self.selected_row = None
        self.cabecalhos = ["Nome", "Auto Abastecimento", "Tipo de Combustível", "Bomba Ativa", "Tanque Nome"]
        self.tela_listar_bombas()

    def tela_listar_bombas(self):
        self.clear_frame()

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(top_frame, text="Lista de Bombas", font=("Arial", 25, "bold")).pack(side="left")

        btn_frame = ctk.CTkFrame(top_frame)
        btn_frame.pack(side="right")

        btn_add = ctk.CTkButton(btn_frame, text="+", command=self.tela_cadastrar_bomba)
        btn_add.pack(side="left", padx=5)

        self.btn_alterar = ctk.CTkButton(btn_frame, text="Alterar", command=self.tela_alterar_bomba, state=tk.DISABLED)
        self.btn_alterar.pack(side="left", padx=5)

        self.btn_excluir = ctk.CTkButton(btn_frame, text="Excluir", command=self.tela_excluir_bomba, state=tk.DISABLED)
        self.btn_excluir.pack(side="left", padx=5)

        try:
            bombas = self.controladorBombaCombustivel.listar_bombas()
            if not bombas:
                Mostra_mensagem("Nenhuma bomba cadastrada.", tipo='info')
                return
        except Exception as e:
            Mostra_mensagem(f"Erro ao listar as bombas: {e}", tipo='erro')
            return

        self.criar_tabela(bombas, self.cabecalhos)
        btn_pesquisar = ctk.CTkButton(self, text="Pesquisar", command=self.pesquisar)
        btn_pesquisar.pack(side="bottom", anchor="se", padx=10, pady=10)

    def criar_tabela(self, dados, cabecalhos):
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=10, pady=20)

        scrollbar_x = ttk.Scrollbar(container, orient="horizontal")
        scrollbar_y = ttk.Scrollbar(container, orient="vertical")

        self.tree = ttk.Treeview(container, columns=cabecalhos, show="headings", height=8,
                                 xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x.config(command=self.tree.xview)
        scrollbar_y.config(command=self.tree.yview)

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        for col in cabecalhos:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.tag_configure('evenrow', background='#242424')
        self.tree.tag_configure('oddrow', background='#2D2E30')

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
            self.btn_excluir.configure(state=tk.NORMAL)
        else:
            self.selected_row = None
            self.btn_alterar.configure(state=tk.DISABLED)
            self.btn_excluir.configure(state=tk.DISABLED)


    def tela_alterar_bomba(self):
        if self.selected_row:
            self.modal_alterar_bomba(self.selected_row)

    def modal_alterar_bomba(self, dados_bomba):
        self.modal = tk.Toplevel(self)
        self.modal.title("Alterar Bomba")

        self.modal.geometry("500x400")
        self.modal.transient(self)
        self.modal.grab_set()
        self.modal.update_idletasks()

        width = self.modal.winfo_width()
        height = self.modal.winfo_height()
        x = (self.modal.winfo_screenwidth() // 2) - (width // 2)
        y = (self.modal.winfo_screenheight() // 2) - (height // 2)
        self.modal.geometry(f'{width}x{height}+{x}+{y}')

        title_label = ctk.CTkLabel(self.modal, text="Alterar Bomba", font=("Arial", 25, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        self.labels = ["Nome", "Tipo de Combustível", "Tanque"]
        self.entries = {}

        global nomes_tanques
        global nomes_combustiveis
        tanques = self.controladorTanqueCombustivel.listar_tanques()
        nomes_tanques = {tanque[0]: tanque[6] for tanque in tanques}  # Dicionário com nomes dos tanques e seus IDs
        nomes_combustiveis = {combustivel[0]: combustivel[3] for combustivel in tanques}

        for i, label in enumerate(self.labels):
            lbl = ctk.CTkLabel(self.modal, text=label)
            lbl.grid(row=i+1, column=0, padx=10, pady=5, sticky='e')

            if label == "Tipo de Combustível":
                self.combustivel_var = tk.StringVar(value=dados_bomba[2])
                entry = ttk.Combobox(self.modal, textvariable=self.combustivel_var, state='disabled', values=list(nomes_combustiveis.values()))
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
            elif label == "Tanque":
                self.tanque_var = tk.StringVar(value=dados_bomba[4])
                entry = ttk.Combobox(self.modal, textvariable=self.tanque_var, values=list(nomes_tanques.keys()))
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
                entry.bind("<<ComboboxSelected>>", self.update_combustivel_entry)
            else:
                entry = ctk.CTkEntry(self.modal, width=120)
                entry.insert(0, dados_bomba[i])
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')

            self.entries[label] = entry

        # Adicionando os switches em uma linha separada
        switch_frame = ctk.CTkFrame(self.modal)
        switch_frame.grid(row=len(self.labels)+1, column=0, columnspan=2, pady=10, sticky='n')

        # Switch para "Auto Abastecimento"
        lbl_auto_abastecimento = ctk.CTkLabel(switch_frame, text="Auto Abastecimento")
        lbl_auto_abastecimento.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.auto_abastecimento_var = ctk.StringVar(value="1" if dados_bomba[1] == "1" else "0")
        switch_auto_abastecimento = ctk.CTkSwitch(switch_frame, text="", variable=self.auto_abastecimento_var, onvalue="1", offvalue="0")
        if dados_bomba[1] == "1":
            switch_auto_abastecimento.select()
        switch_auto_abastecimento.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Switch para "Bomba Ativa"
        lbl_bomba_ativa = ctk.CTkLabel(switch_frame, text="Bomba Ativa")
        lbl_bomba_ativa.grid(row=0, column=2, padx=10, pady=5, sticky='e')
        self.bomba_ativa_var = ctk.StringVar(value="1" if dados_bomba[3] == "1" else "0")
        switch_bomba_ativa = ctk.CTkSwitch(switch_frame, text="", variable=self.bomba_ativa_var, onvalue="1", offvalue="0")
        if dados_bomba[3] == "1":
            switch_bomba_ativa.select()
        switch_bomba_ativa.grid(row=0, column=3, padx=10, pady=5, sticky='w')

        update_button = ctk.CTkButton(self.modal, text="Atualizar", command=self.tela_atualizar_bomba)
        update_button.grid(row=len(self.labels)+2, column=0, columnspan=2, pady=20)

        for i in range(len(self.labels) + 3):
            self.modal.grid_rowconfigure(i, weight=1)
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=1)


    def tela_atualizar_bomba(self):
        nomeBomba = self.entries["Nome"].get()
        autoAbastecimento = self.auto_abastecimento_var.get()
        tipoCombustivel = self.combustivel_var.get()
        bombaAtiva = self.bomba_ativa_var.get()
        tanque_nome = self.tanque_var.get()
        identificadorTanque = nomes_tanques[tanque_nome]  # Obter o ID do tanque a partir do nome
        identificadorBomba = self.selected_row[5]
        print

        print(nomeBomba, autoAbastecimento, tipoCombustivel, bombaAtiva, identificadorTanque, identificadorBomba)

        if not nomeBomba or not autoAbastecimento or not tipoCombustivel or not bombaAtiva or not identificadorTanque:
            Mostra_mensagem("Todos os campos devem ser preenchidos!", tipo='erro')
            return

        try:
            resultado = self.controladorBombaCombustivel.atualizar_bomba(autoAbastecimento, tipoCombustivel, bombaAtiva, identificadorTanque, nomeBomba, identificadorBomba)
            if resultado:
                Mostra_mensagem("Bomba atualizada com sucesso!", tipo='info')
                self.modal.destroy()
                self.pesquisar()
            else:
                Mostra_mensagem("Erro ao atualizar a bomba.", tipo='erro')
        except Exception as e:
            Mostra_mensagem(f"Erro ao atualizar a bomba: {e}", tipo='erro')

    def update_combustivel_entry(self, event):
        # Atualiza o campo de tipo de combustível quando uma bomba é selecionada
        tanque = self.tanque_var.get()
        if tanque:
            self.combustivel_var.set(nomes_combustiveis[tanque])

    def tela_excluir_bomba(self):
        if self.selected_row:
            identificadorBomba = self.selected_row[5]
            try:
                resultado = self.controladorBombaCombustivel.remover_bomba(identificadorBomba)
                if resultado:
                    Mostra_mensagem("Bomba excluída com sucesso!", tipo='info')
                    self.pesquisar()
                else:
                    Mostra_mensagem("Erro ao excluir a bomba.", tipo='erro')
            except Exception as e:
                Mostra_mensagem(f"Erro ao excluir a bomba: {e}", tipo='erro')
                return
            self.btn_alterar.configure(state=tk.DISABLED)
            self.btn_excluir.configure(state=tk.DISABLED)

    def pesquisar(self):
        try:
            bombas = self.controladorBombaCombustivel.listar_bombas()
        except Exception as e:
            Mostra_mensagem(f"Erro ao pesquisar as bombas: {e}", tipo='erro')
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, row in enumerate(bombas):
            self.tree.insert('', 'end', values=row, tags=('evenrow' if index % 2 == 0 else 'oddrow'))

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def tela_cadastrar_bomba(self):
        self.modal_cadastrar_bomba()

    def modal_cadastrar_bomba(self):
        self.modal = tk.Toplevel(self)
        self.modal.title("Cadastrar Nova Bomba")

        self.modal.geometry("500x400")
        self.modal.transient(self)
        self.modal.grab_set()
        self.modal.update_idletasks()

        width = self.modal.winfo_width()
        height = self.modal.winfo_height()
        x = (self.modal.winfo_screenwidth() // 2) - (width // 2)
        y = (self.modal.winfo_screenheight() // 2) - (height // 2)
        self.modal.geometry(f'{width}x{height}+{x}+{y}')

        global nomes_tanques
        global nomes_combustiveis
        tanques = self.controladorTanqueCombustivel.listar_tanques()
        nomes_tanques = {tanque[0]: tanque[6] for tanque in tanques}  # Dicionário com nomes dos tanques e seus IDs
        nomes_combustiveis = {combustivel[0]: combustivel[3] for combustivel in tanques}

        title_label = ctk.CTkLabel(self.modal, text="Cadastrar Nova Bomba", font=("Arial", 25, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='n')

        self.labels = ["Nome", "Tipo de Combustível", "Tanque"]
        self.entries = {}

        for i, label in enumerate(self.labels):
            lbl = ctk.CTkLabel(self.modal, text=label)
            lbl.grid(row=i+1, column=0, padx=10, pady=5, sticky='e')

            if label == "Tipo de Combustível":
                self.combustivel_var = tk.StringVar()
                entry = ttk.Combobox(self.modal, textvariable=self.combustivel_var, state='disabled', values=list(nomes_combustiveis.values()))
            elif label == "Tanque":
                self.tanque_var = tk.StringVar()
                entry = ttk.Combobox(self.modal, textvariable=self.tanque_var, values=list(nomes_tanques.keys()))
                entry.bind("<<ComboboxSelected>>", self.update_combustivel_entry)
            else:
                entry = ctk.CTkEntry(self.modal, width=120)

            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
            self.entries[label] = entry

        # Adicionando os switches em uma linha separada
        switch_frame = ctk.CTkFrame(self.modal)
        switch_frame.grid(row=len(self.labels)+1, column=0, columnspan=2, pady=10, sticky='n')

        lbl_auto_abastecimento = ctk.CTkLabel(switch_frame, text="Auto Abastecimento")
        lbl_auto_abastecimento.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.auto_abastecimento_var = ctk.StringVar(value=0)
        switch_auto_abastecimento = ctk.CTkSwitch(switch_frame, text="", variable=self.auto_abastecimento_var, onvalue=1, offvalue=0)
        switch_auto_abastecimento.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        lbl_bomba_ativa = ctk.CTkLabel(switch_frame, text="Bomba Ativa")
        lbl_bomba_ativa.grid(row=0, column=2, padx=10, pady=5, sticky='e')
        self.bomba_ativa_var = ctk.StringVar(value=1)
        switch_bomba_ativa = ctk.CTkSwitch(switch_frame, text="", variable=self.bomba_ativa_var, onvalue=1, offvalue=0)
        switch_bomba_ativa.grid(row=0, column=3, padx=10, pady=5, sticky='w')

        cadastrar_button = ctk.CTkButton(self.modal, text="Cadastrar", command=self.salvar_nova_bomba)
        cadastrar_button.grid(row=len(self.labels)+2, column=0, columnspan=2, pady=20, sticky='n')

        for i in range(len(self.labels) + 3):
            self.modal.grid_rowconfigure(i, weight=1)
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=1)

        # Centraliza os widgets no modal
        self.modal.grid_rowconfigure(len(self.labels) + 3, weight=1)
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=1)

    def salvar_nova_bomba(self):
        nomeBomba = self.entries["Nome"].get()
        autoAbastecimento = self.auto_abastecimento_var.get()
        tipoCombustivel = self.combustivel_var.get()
        bombaAtiva = self.bomba_ativa_var.get()
        tanque_nome = self.entries["Tanque"].get()
        tanque_id = nomes_tanques[tanque_nome]

        print(nomeBomba, autoAbastecimento, tipoCombustivel, bombaAtiva, tanque_id)
        if not nomeBomba or not autoAbastecimento or not tipoCombustivel or not bombaAtiva or not tanque_id:
            Mostra_mensagem("Todos os campos devem ser preenchidos!", tipo='erro')
            return

        try:
            resultado = self.controladorBombaCombustivel.adicionar_bomba(autoAbastecimento, tipoCombustivel, bombaAtiva, tanque_id, nomeBomba)
            Mostra_mensagem("Nova bomba cadastrada com sucesso!", tipo='info')
            self.modal.destroy()
            self.pesquisar()
        except Exception as e:
            Mostra_mensagem(f"Erro ao cadastrar a nova bomba: {e}", tipo='erro')


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1200x800")
    app = TelaBombaCombustivel(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
