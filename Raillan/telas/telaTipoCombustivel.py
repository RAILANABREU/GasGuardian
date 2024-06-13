from controladores.controladorTipoCombustivel import ControladorTipoCombustivel
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class TelaTipoCombustivel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controlador = ControladorTipoCombustivel()
        self.selected_row = None
        self.cabecalhos = ["Nome do Combustível", "Preço"]
        self.criar_tela_tipo_combustivel()

    def mostra_mensagem(self, mensagem, tipo='erro'):
        if tipo == 'erro':
            messagebox.showerror("Erro", mensagem)
        elif tipo == 'info':
            messagebox.showinfo("Informação", mensagem)

    def criar_tela_tipo_combustivel(self):
        self.clear_frame()

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", pady=20, padx=20)

        ctk.CTkLabel(top_frame, text="Tipos de Combustível", font=("Arial", 25, "bold")).pack(side="left")

        btn_frame = ctk.CTkFrame(top_frame)
        btn_frame.pack(side="right")

        btn_add = ctk.CTkButton(btn_frame, text="+", command=self.modal_cadastrar_tipo_combustivel)
        btn_add.pack(side="left", padx=5)

        self.btn_alterar = ctk.CTkButton(btn_frame, text="Alterar", command=self.tela_alterar_tipo_combustivel, state=tk.DISABLED)
        self.btn_alterar.pack(side="left", padx=5)

        self.btn_excluir = ctk.CTkButton(btn_frame, text="Excluir", command=self.tela_excluir_tipo_combustivel, state=tk.DISABLED)
        self.btn_excluir.pack(side="left", padx=5)

        try:
            tipo_combustivel = self.controlador.listar_tipo_combustivel()
            if not tipo_combustivel:
                self.mostra_mensagem("Nenhum tipo de combustível cadastrado.", 'info')
                return
        except Exception as e:
            self.mostra_mensagem(f"Erro ao listar tipos de combustível: {e}", 'erro')

        self.criar_tabela(tipo_combustivel, self.cabecalhos)

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

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def modal_cadastrar_tipo_combustivel(self):
        self.modal = tk.Toplevel(self)
        self.modal.title("Cadastrar Novo Tipo de Combustível")
        self.centralize_modal(self.modal, 500, 400)

        ctk.CTkLabel(self.modal, text="Cadastrar Novo Tipo de Combustível", font=("Arial", 16, "bold")).pack(pady=20)

        fields = ["Nome do Combustível", "Preço"]
        entries = {}
        for i, field in enumerate(fields):
            ctk.CTkLabel(self.modal, text=field).pack()
            entry = ctk.CTkEntry(self.modal, width=250)
            if field == "Preço":
                entry.configure(validate="key", validatecommand=(self.register(self.validate_preco), '%P'))
            entry.pack(pady=10)
            entries[field] = entry

        ctk.CTkButton(self.modal, text="Salvar", command=lambda: self.salvar_tipo_combustivel(entries)).pack(pady=20)

    def salvar_tipo_combustivel(self, entries):
        nome = entries["Nome do Combustível"].get().strip()
        preco = entries["Preço"].get().strip()
        if not nome or not preco:
            self.mostra_mensagem("Todos os campos devem ser preenchidos!", 'erro')
            return
        try:
            preco_formatado = "{:.2f}".format(float(preco))
            self.controlador.adicionar_tipo_combustivel(nome, preco_formatado)
            self.mostra_mensagem("Tipo de combustível cadastrado com sucesso!", 'info')
            self.modal.destroy()
            self.pesquisar()
        except Exception as e:
            self.mostra_mensagem(f"Erro ao cadastrar tipo de combustível: {e}", 'erro')

    def centralize_modal(self, modal, width, height):
        modal.geometry(f"{width}x{height}+{(modal.winfo_screenwidth() // 2) - (width // 2)}+{(modal.winfo_screenheight() // 2) - (height // 2)}")

    def tela_alterar_tipo_combustivel(self):
        if not self.selected_row:
            self.mostra_mensagem("Selecione um tipo de combustível na lista para alterar!", 'info')
            return

        self.modal = tk.Toplevel(self)
        self.modal.title("Alterar Tipo de Combustível")
        self.centralize_modal(self.modal, 500, 400)

        ctk.CTkLabel(self.modal, text="Alterar Tipo de Combustível", font=("Arial", 16, "bold")).pack(pady=20)

        fields = ["Nome do Combustível", "Preço"]
        entries = {}
        for i, field in enumerate(fields):
            ctk.CTkLabel(self.modal, text=field).pack()
            entry = ctk.CTkEntry(self.modal, width=250)
            if field == "Preço":
                entry.configure(validate="key", validatecommand=(self.register(self.validate_preco), '%P'))
            entry.insert(0, self.selected_row[i])
            entry.pack(pady=10)
            entries[field] = entry

        ctk.CTkButton(self.modal, text="Salvar Alterações", command=lambda: self.salvar_alteracoes_tipo_combustivel(entries)).pack(pady=20)

    def salvar_alteracoes_tipo_combustivel(self, entries):
        nome = entries["Nome do Combustível"].get().strip()
        preco = entries["Preço"].get().strip()
        if not nome or not preco:
            self.mostra_mensagem("Todos os campos devem ser preenchidos!", 'erro')
            return
        try:
            preco_formatado = "{:.2f}".format(float(preco))
            self.controlador.atualizar_tipo_combustivel(nome, preco_formatado)
            self.mostra_mensagem("Tipo de combustível atualizado com sucesso!", 'info')
            self.modal.destroy()
            self.pesquisar()
        except Exception as e:
            self.mostra_mensagem(f"Erro ao atualizar tipo de combustível: {e}", 'erro')

    def tela_excluir_tipo_combustivel(self):    
        self.modal = tk.Toplevel(self)
        self.modal.title("Excluir Tipo de Combustível")
        self.centralize_modal(self.modal, 700, 200)

        ctk.CTkLabel(self.modal, text=f"Tem certeza que deseja excluir o tipo de combustível {self.selected_row[0]}?", font=("Arial", 16)).pack(pady=10)
        ctk.CTkButton(self.modal, text="Excluir", command=self.excluir_tipo_combustivel).pack(side="left", padx=100, pady=20)
        ctk.CTkButton(self.modal, text="Cancelar", command=self.modal.destroy).pack(side="right", padx=100, pady=20)

    def excluir_tipo_combustivel(self):
        try:
            self.controlador.remover_tipo_combustivel(self.selected_row[0])
            self.mostra_mensagem("Tipo de combustível excluído com sucesso!", 'info')
            self.modal.destroy()
            self.pesquisar()
        except Exception as e:
            self.mostra_mensagem(f"Erro ao excluir tipo de combustível: {e}", 'erro')

    def pesquisar(self):
        try:
            tipo_combustivel = self.controlador.listar_tipo_combustivel()
        except Exception as e:
            self.mostra_mensagem(f"Erro ao pesquisar os tipos de combustível: {e}", tipo='erro')
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, row in enumerate(tipo_combustivel):
            self.tree.insert('', 'end', values=row, tags=('evenrow' if index % 2 == 0 else 'oddrow'))

    def validate_preco(self, value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            float(value_if_allowed)
            parts = value_if_allowed.split(".")
            if len(parts) == 2 and len(parts[1]) > 2:
                return False
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    root = ctk.CTk()
    root.geometry("1200x800")
    app = TelaTipoCombustivel(root)
    app.pack(fill="both", expand=True)
    app.mainloop()