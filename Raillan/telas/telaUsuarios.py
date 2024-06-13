import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

from controladores.controladorUsuario import ControladorUsuario


class TelaUsuario(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_row = None
        self.cabecalhos = ["Nome", "CPF", "Email", "Telefone"]
        self.controladorUsuario = ControladorUsuario()
        self.Criar_tela_usuario()

    def mostra_mensagem(self, mensagem, tipo='erro'):
        if tipo == 'erro':
            messagebox.showerror("Erro", mensagem, icon='error')
        elif tipo == 'info':
            messagebox.showinfo("Informação", mensagem, icon='info')

    def Criar_tela_usuario(self):
        self.clear_frame()

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(top_frame, text="Usuarios", font=("Arial", 25, "bold")).pack(side="left")

        btn_frame = ctk.CTkFrame(top_frame)
        btn_frame.pack(side="right")

        btn_add = ctk.CTkButton(btn_frame, text="+", command=self.tela_cadastrar_usuario)
        btn_add.pack(side="left", padx=5)

        self.btn_alterar = ctk.CTkButton(btn_frame, text="Alterar", command=self.tela_alterar_usuario, state=tk.DISABLED)
        self.btn_alterar.pack(side="left", padx=5)

        self.btn_excluir = ctk.CTkButton(btn_frame, text="Excluir", command=self.tela_excluir_usuario, state=tk.DISABLED)
        self.btn_excluir.pack(side="left", padx=5)

        try:
            usuarios = self.controladorUsuario.listar_usuarios()
            if not usuarios:
                self.mostra_mensagem("Nenhuma usuario cadastrada.", tipo='info')
                return
        except Exception as e:
            self.mostra_mensagem(f"Erro ao listar os usuarios: {e}", tipo='erro')
            return

        self.criar_tabela(usuarios, self.cabecalhos)
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

    def tela_alterar_usuario(self):
        if self.selected_row:
            self.modal_alterar_usuario(self.selected_row)

    def modal_alterar_usuario(self, dados_usuario):
        self.modal = tk.Toplevel(self)
        self.modal.title("Alterar Usuário")

        self.modal.geometry("500x400")
        self.modal.transient(self)
        self.modal.grab_set()
        self.modal.update_idletasks()

        width = self.modal.winfo_width()
        height = self.modal.winfo_height()
        x = (self.modal.winfo_screenwidth() // 2) - (width // 2)
        y = (self.modal.winfo_screenheight() // 2) - (height // 2)
        self.modal.geometry(f'{width}x{height}+{x}+{y}')

        title_label = ctk.CTkLabel(self.modal, text="Alterar Usuário", font=("Arial", 25, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        self.labels = ["Nome", "CPF", "Telefone", "Email", "É Gestor"]
        self.entries = {}

        for i, label in enumerate(self.labels):
            lbl = ctk.CTkLabel(self.modal, text=label)
            lbl.grid(row=i+1, column=0, padx=10, pady=5, sticky='e')

            if label == "É Gestor":
                self.is_gestor_var = ctk.StringVar(value="off")
                entry = ctk.CTkSwitch(self.modal, text="", variable=self.is_gestor_var, onvalue="on", offvalue="off")
            else:
                entry = ctk.CTkEntry(self.modal, width=120)
                entry.insert(0, dados_usuario[i])
                if label == "CPF":
                    entry.configure(state='disabled')
                    entry.bind("<KeyRelease>", self.format_cpf)
                if label == "Telefone":
                    entry.bind("<KeyRelease>", self.format_telefone)

            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
            self.entries[label] = entry

        update_button = ctk.CTkButton(self.modal, text="Atualizar", command=self.tela_atualizar_usuario)
        update_button.grid(row=len(self.labels)+1, column=0, columnspan=2, pady=20)

        for i in range(len(self.labels) + 2):
            self.modal.grid_rowconfigure(i, weight=1)
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=1)

    def tela_atualizar_usuario(self):
        nome = self.entries["Nome"].get()
        cpf = self.entries["CPF"].get()
        email = self.entries["Email"].get()
        telefone = self.entries["Telefone"].get()
        is_gestor = self.is_gestor_var.get()
        # Remover caracteres especiais do CPF e telefone
        cpf = re.sub(r'\D', '', cpf)
        telefone = re.sub(r'\D', '', telefone)
        if not nome or not cpf or not email or not telefone:
            self.mostra_mensagem("Todos os campos devem ser preenchidos!", tipo='erro')
            return

        try:
            resultado = self.controladorUsuario.atualizar_usuario(cpf, email, nome, telefone, is_gestor)
            if resultado:
                self.mostra_mensagem("Usuário atualizado com sucesso!", tipo='info')
                self.modal.destroy()
                self.pesquisar()
            else:
                self.mostra_mensagem("Erro ao atualizar o usuário.", tipo='erro')
        except Exception as e:
            self.mostra_mensagem(f"Erro ao atualizar o usuário: {e}", tipo='erro')

    def tela_excluir_usuario(self):
        if self.selected_row:
            identificador_usuario = self.selected_row[0]
            try:
                resultado = self.controladorUsuario.remover_usuario(identificador_usuario)
                if resultado:
                    self.mostra_mensagem("Usuário excluído com sucesso!", tipo='info')
                    self.pesquisar()
                else:
                    self.mostra_mensagem("Erro ao excluir o usuário.", tipo='erro')
            except Exception as e:
                self.mostra_mensagem(f"Erro ao excluir o usuário: {e}", tipo='erro')
                return
            self.btn_alterar.configure(state=tk.DISABLED)
            self.btn_excluir.configure(state=tk.DISABLED)

    def pesquisar(self):
        try:
            usuarios = self.controladorUsuario.listar_usuarios()
        except Exception as e:
            self.mostra_mensagem(f"Erro ao pesquisar os usuários: {e}", tipo='erro')
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, row in enumerate(usuarios):
            self.tree.insert('', 'end', values=row, tags=('evenrow' if index % 2 == 0 else 'oddrow'))

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def tela_cadastrar_usuario(self):
        self.modal_cadastrar_usuario()

    def modal_cadastrar_usuario(self):
        self.modal = tk.Toplevel(self)
        self.modal.title("Cadastrar Novo Usuário")

        self.modal.geometry("500x400")
        self.modal.transient(self)
        self.modal.grab_set()
        self.modal.update_idletasks()

        width = self.modal.winfo_width()
        height = self.modal.winfo_height()
        x = (self.modal.winfo_screenwidth() // 2) - (width // 2)
        y = (self.modal.winfo_screenheight() // 2) - (height // 2)
        self.modal.geometry(f'{width}x{height}+{x}+{y}')

        title_label = ctk.CTkLabel(self.modal, text="Cadastrar Novo Usuário", font=("Arial", 25, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        self.labels = ["Nome", "CPF", "Email", "Telefone", "Senha", "Confirmar Senha", "É Gestor"]
        self.entries = {}

        for i, label in enumerate(self.labels):
            lbl = ctk.CTkLabel(self.modal, text=label)
            lbl.grid(row=i+1, column=0, padx=10, pady=5, sticky='e')

            if label == "É Gestor":
                self.is_gestor_var = ctk.StringVar(value="off")
                entry = ctk.CTkSwitch(self.modal, text="", variable=self.is_gestor_var, onvalue=1, offvalue=0)
            else:
                entry = ctk.CTkEntry(self.modal, width=120, placeholder_text=f"{label.lower()}")
                if label == "CPF":
                    entry.bind("<KeyRelease>", self.format_cpf)
                if label == "Telefone":
                    entry.bind("<KeyRelease>", self.format_telefone)

            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
            self.entries[label] = entry

        cadastrar_button = ctk.CTkButton(self.modal, text="Cadastrar", command=self.salvar_novo_usuario)
        cadastrar_button.grid(row=len(self.labels)+1, column=0, columnspan=2, pady=20)

        for i in range(len(self.labels) + 2):
            self.modal.grid_rowconfigure(i, weight=1)
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=1)

    def salvar_novo_usuario(self):
        nome = self.entries["Nome"].get()
        cpf = self.entries["CPF"].get()
        email = self.entries["Email"].get()
        telefone = self.entries["Telefone"].get()
        senha = self.entries["Senha"].get()
        confirmar_senha = self.entries["Confirmar Senha"].get()
        is_gestor = self.is_gestor_var.get()

            # Remover caracteres especiais do CPF e telefone
        cpf = re.sub(r'\D', '', cpf)
        telefone = re.sub(r'\D', '', telefone)

        if not nome or not cpf or not email or not telefone or not senha or not confirmar_senha:
            self.mostra_mensagem("Todos os campos devem ser preenchidos!", tipo='erro')
            return

        if senha != confirmar_senha:
            self.mostra_mensagem("As senhas não coincidem!", tipo='erro')
            return

        try:
            print(nome, cpf, email, telefone, senha, is_gestor)
            resultado = self.controladorUsuario.adicionar_usuario( cpf, email, nome, telefone, senha, is_gestor)
            if resultado:
                self.mostra_mensagem("Novo usuário cadastrado com sucesso!", tipo='info')
                self.modal.destroy()
                self.pesquisar()
            else:
                self.mostra_mensagem("Erro ao cadastrar o usuário.", tipo='erro')
        except Exception as e:
            self.mostra_mensagem(f"Erro ao cadastrar o usuário: {e}", tipo='erro')

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

    def format_telefone(self, event):
        entry = event.widget
        telefone = re.sub(r'\D', '', entry.get())
        formatted_telefone = telefone
        if len(telefone) > 2:
            formatted_telefone = f"({telefone[:2]}) {telefone[2:7]}"
        if len(telefone) > 7:
            formatted_telefone = f"{formatted_telefone}-{telefone[7:11]}"
        elif len(telefone) > 2:
            formatted_telefone = f"({telefone[:2]}) {telefone[2:]}"
        entry.delete(0, tk.END)
        entry.insert(0, formatted_telefone)



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1200x800")
    app = TelaUsuario(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
