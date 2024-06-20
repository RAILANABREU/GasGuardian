import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from controladores.controladorTipoCombustivel import ControladorTipoCombustivel
from controladores.controladorTanqueCombustivel import ControladorTanqueCombustivel
from controladores.controladorBombaCombustivel import ControladorBombaCombustivel
from controladores.controladorAbastecimento import ControladorAbastecimento
from entidades.sessao import Sessao
import customtkinter as ctk
from datetime import datetime

class TelaAbastecimento(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controladorBombaCombustivel = ControladorBombaCombustivel()
        self.controladorTipoCombustivel = ControladorTipoCombustivel()
        self.controladorTanqueCombustivel = ControladorTanqueCombustivel()
        self.controladorAbastecimento = ControladorAbastecimento()
        self.cpf_funcionario = Sessao.get_usuario_logado()[2]

        self.create_main_button()
        print(self.cpf_funcionario)

    def mostra_mensagem(self, mensagem, tipo='erro'):
        if tipo == 'erro':
            messagebox.showerror("Erro", mensagem)
        elif tipo == 'info':
            messagebox.showinfo("Informação", mensagem)
    
    def centralize_modal(self, modal, width, height):
        modal.geometry(f"{width}x{height}+{(modal.winfo_screenwidth()//2) - (width//2)}+{(modal.winfo_screenheight()//2) - (height//2)}")

    def create_main_button(self):
        self.registrar_button = ctk.CTkButton(self, text="Registrar Abastecimento", command=self.modal_registrar_abastecimento, font=("Arial", 20, "bold"), width=200, height=100)
        self.registrar_button.pack(expand=True, padx=20, pady=20)

    def modal_registrar_abastecimento(self):
        # Criação da janela modal
        self.modal = tk.Toplevel(self)
        self.modal.title("Registrar Abastecimento")
        self.centralize_modal(self.modal, 500, 400)

        # Título da modal
        title_label = ctk.CTkLabel(self.modal, text="Registrar Abastecimento", font=("Arial", 25, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        # Rótulos dos campos
        self.labels = ["Bomba", "Tipo de Combustível", "Preço", "Litros abastecidos"]
        self.entries = {}

        # Obtenção dos dados das bombas e combustíveis
        global combustivel_data
        global dados_bomba
        global combustivel_preco
        bombas = self.controladorBombaCombustivel.listar_bombas_ativas()
        dados_bomba = {bomba[0]: bomba[3] for bomba in bombas}
        combustivel_data = {bomba[0]: bomba[1] for bomba in bombas}
        combustivel_preco = {bomba[0]: bomba[2] for bomba in bombas}

        # Criação dos campos de entrada
        for i, label in enumerate(self.labels):
            lbl = ctk.CTkLabel(self.modal, text=label)
            lbl.grid(row=i+1, column=0, padx=10, pady=5, sticky='e')

            if label == "Bomba":
                self.bomba_var = tk.StringVar()
                entry = ttk.Combobox(self.modal, textvariable=self.bomba_var, values=list(dados_bomba.keys()))
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
                entry.bind("<<ComboboxSelected>>", self.update_combustivel_entry)
            elif label == "Tipo de Combustível":
                self.combustivel_var = tk.StringVar()
                entry = ctk.CTkEntry(self.modal, textvariable=self.combustivel_var, state='disabled')
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
            elif label == "Preço":
                self.preco_var = tk.StringVar()
                vcmd = (self.modal.register(self.validate_float), '%P')
                entry = ctk.CTkEntry(self.modal, textvariable=self.preco_var, width=120, validate='key', validatecommand=vcmd)
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')
                entry.bind("<KeyRelease>", self.calcula_litros)
            else:
                entry = ctk.CTkEntry(self.modal, width=120, state='readonly')
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='we')

            self.entries[label] = entry

        # Botão de cadastro
        cadastrar_button = ctk.CTkButton(self.modal, text="Cadastrar", command=self.salvar_abastecimento)
        cadastrar_button.grid(row=len(self.labels)+1, column=0, columnspan=2, pady=20)

    def validate_float(self, value_if_allowed):
        # Valida se a entrada é um número float
        if not value_if_allowed:
            return True
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False

    def update_combustivel_entry(self, event):
        # Atualiza o campo de tipo de combustível quando uma bomba é selecionada
        bomba = self.bomba_var.get()
        if bomba:
            self.combustivel_var.set(combustivel_data[bomba])
            self.calcula_litros(None)
        else:
            self.mostra_mensagem("Selecione uma bomba válida!", tipo='erro')
    def calcula_litros(self, event):
        # Calcula os litros abastecidos com base no preço e no preço do combustível da bomba selecionada
        try:
            valor = float(self.preco_var.get())
        except ValueError:
            self.entries["Litros abastecidos"].delete(0, tk.END)
            self.entries["Litros abastecidos"].insert(0, "0.000")
            self.entries["Litros abastecidos"].configure(state='readonly')
            return

        bomba = self.bomba_var.get()
        if bomba and bomba in dados_bomba:
            preco_combustivel = combustivel_preco[bomba]  # Pega o preço do combustível da bomba
            if preco_combustivel != 0:
                litros = valor / preco_combustivel
                self.entries["Litros abastecidos"].configure(state='normal')
                self.entries["Litros abastecidos"].delete(0, tk.END)
                self.entries["Litros abastecidos"].insert(0, f"{litros:.3f}")
                self.entries["Litros abastecidos"].configure(state='readonly')
        else:
            self.entries["Litros abastecidos"].delete(0, tk.END)
            self.entries["Litros abastecidos"].insert(0, "0.000")
            self.entries["Litros abastecidos"].configure(state='readonly')



    def salvar_abastecimento(self):
        nomeBomba = self.entries["Bomba"].get()
        idBomba = dados_bomba[nomeBomba]
        tipoCombustivel = self.combustivel_var.get()
        data = datetime.now()
        data_formatada = data.strftime("%Y-%m-%d %H:%M:%S")
        preco = self.entries["Preço"].get()
        litros = self.entries["Litros abastecidos"].get()

        if not nomeBomba or not tipoCombustivel or not preco:
            self.mostra_mensagem("Todos os campos devem ser preenchidos!", tipo='erro')
            return

        try:
            resultado = self.controladorAbastecimento.adicionar_abastecimento(idBomba, tipoCombustivel, data_formatada, preco, litros, self.cpf_funcionario)
            self.mostra_mensagem("Abastecimento registrado com sucesso!", tipo='info')
            self.modal.destroy()
        except Exception as e:
            print(Exception, e)
            self.mostra_mensagem(f"Erro ao registrar abastecimento: {e}", tipo='erro')

    def centralize_modal(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def mostra_mensagem(self, mensagem, tipo='info'):
        if tipo == 'info':
            messagebox.showinfo("Informação", mensagem)
        elif tipo == 'erro':
            messagebox.showerror("Erro", mensagem)

    def pesquisar(self):
        pass  # implementar função de pesquisa

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Sistema de Abastecimento")
    root.geometry("1200x800")
    app = TelaAbastecimento(root)
    app.pack(fill="both", expand=True)
    root.mainloop()