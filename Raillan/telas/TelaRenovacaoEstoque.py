import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from controladores.controladorTanqueCombustivel import ControladorTanqueCombustivel

class TelaRenovacaoEstoque(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controladorTanqueCombustivel = ControladorTanqueCombustivel()
        self.criar_tela_renovacao_estoque()

    def criar_tela_renovacao_estoque(self):
        # Limpa a tela antes de recriar os elementos
        for widget in self.winfo_children():
            widget.destroy()

        # Frame para o título
        title_frame = ctk.CTkFrame(self)
        title_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(title_frame, text="Renovação de Estoque", font=("Arial", 25, "bold")).pack(side="left", padx=10)

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="both", expand=True)

        # Obtendo os dados dos tanques
        tanques = self.controladorTanqueCombustivel.listar_tanques()

        # Criando barra de progresso e botão para cada tanque
        for index, tanque in enumerate(tanques):
            nome, porcentagemAlerta, capacidade, combustivel, volume_atual, status, id = tanque
            frame_tanque = ctk.CTkFrame(top_frame, corner_radius=10)
            frame_tanque.pack(fill="x", padx=20, pady=10)

            label_tanque = ctk.CTkLabel(frame_tanque, text=f"{nome} ({combustivel}) - {volume_atual:.2f}/{capacidade} L")
            label_tanque.pack(side="left", padx=10)

            # Botão para abastecimento
            btn_abastecer = ctk.CTkButton(frame_tanque, text="Abastecer", 
                command=lambda tanque_id=id: self.abrir_modal_abastecimento(tanque_id))
            btn_abastecer.pack(side="right", padx=10, pady=10)

            # Configurando a cor da barra de progresso
            progress_color = "red" if status < porcentagemAlerta else "blue"
            progress_bar = ctk.CTkProgressBar(frame_tanque, orientation="horizontal", progress_color=progress_color, width=350, height=10)
            progress_bar.set(status / 100)  # Convertendo de porcentagem para decimal
            progress_bar.pack(side="right", fill="none", expand=False, padx=10)

        # Frame para o botão de pesquisa
        pesquisar_frame = ctk.CTkFrame(self)
        pesquisar_frame.pack(fill="x", pady=10)

        # Botão para atualizar a lista de tanques
        btn_atualizar = ctk.CTkButton(pesquisar_frame, text="Atualizar", command=self.criar_tela_renovacao_estoque)
        btn_atualizar.pack(side="right", padx=10)

    def abrir_modal_abastecimento(self, tanque_id):
        modal = ctk.CTkToplevel(self)
        modal.title("Abastecimento de Tanque")
        modal.geometry("500x400")

        # Configuração do título
        titulo_label = ctk.CTkLabel(modal, text="Abastecer Tanque", font=("Arial", 25))
        titulo_label.pack(pady=20)

        # Buscar informações do tanque
        tanque = self.controladorTanqueCombustivel.buscar_tanque(tanque_id)
        if not tanque:
            self.mostra_mensagem("Tanque não encontrado!", tipo='erro')
            modal.destroy()  # Fecha o modal se o tanque não for encontrado
            return

        # Widgets para exibir informações (campos desabilitados para edição)
        tanque_id_label = ctk.CTkLabel(modal, text="Nome do Tanque")
        tanque_id_label.pack()
        tanque_id_entry = ctk.CTkEntry(modal, width=200, height=30)
        tanque_id_entry.pack(pady=5)
        tanque_id_entry.insert(0, tanque[5])
        tanque_id_entry.configure(state='disabled')  # Desabilita a edição após inserir o texto

        combustivel_label = ctk.CTkLabel(modal, text="Combustível")
        combustivel_label.pack()
        combustivel_entry = ctk.CTkEntry(modal, width=200, height=30)
        combustivel_entry.pack(pady=5)
        combustivel_entry.insert(0, tanque[3])
        combustivel_entry.configure(state='disabled')  # Desabilita a edição após inserir o texto

        # Campo de entrada para a quantidade de abastecimento
        entrada_abastecimento_label = ctk.CTkLabel(modal, text="Quantidade de Abastecimento")
        entrada_abastecimento_label.pack()
        entrada_abastecimento = ctk.CTkEntry(modal, placeholder_text="Digite a quantidade a abastecer", width=200, height=30)
        entrada_abastecimento.pack(pady=10)
        
        # Validação para aceitar apenas números
        def validar_entrada(texto):
            return texto.isdigit() or texto == ""
        
        vcmd = (self.register(validar_entrada), '%P')
        entrada_abastecimento.configure(validate="key", validatecommand=vcmd)

        # Botão para confirmar o abastecimento
        confirm_button = ctk.CTkButton(modal, text="Confirmar",
                                    command=lambda: self.confirmar_abastecimento(modal, tanque_id, entrada_abastecimento.get()))
        confirm_button.pack(pady=20)

    def confirmar_abastecimento(self, modal, tanque_id, quantidade):
        try:
            quantidade = float(quantidade)
            self.controladorTanqueCombustivel.renovar_estoque(tanque_id, quantidade)
            self.mostra_mensagem("Abastecimento realizado com sucesso!", tipo='info')
            modal.destroy()  # Fecha o modal após confirmar o abastecimento
            self.criar_tela_renovacao_estoque()  # Atualiza a tela principal
        except Exception as e:
            self.mostra_mensagem(f"Erro: {e}", tipo='erro')

    def mostra_mensagem(self, mensagem, tipo='erro'):
        if tipo == 'erro':
            messagebox.showerror("Erro", mensagem, icon='error')
        elif tipo == 'info':
            messagebox.showinfo("Informação", mensagem, icon='info')

