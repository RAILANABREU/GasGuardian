import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from controladores.controladorTanqueCombustivel import ControladorTanqueCombustivel

class TelaRenovacaoEstoque(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__controlador_tanque_combustivel = ControladorTanqueCombustivel()
        self.criar_tela_renovacao_estoque()

    def criar_tela_renovacao_estoque(self):
        # Frame para o título
        title_frame = ctk.CTkFrame(self)
        title_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(title_frame, text="Renovação de Estoque", font=("Arial", 25, "bold")).pack(side="left", padx=10)

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="both", expand=True)

        # Obtendo os dados dos tanques
        tanques = self.__controlador_tanque_combustivel.listar_tanques()

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

    def abrir_modal_abastecimento(self, tanque_id):
        modal = ctk.CTkToplevel(self)
        modal.title("Abastecimento de Tanque")
        modal.geometry("300x200")

        # Buscar informações do tanque
        tanque = self.__controlador_tanque_combustivel.buscar_tanque(tanque_id)
        if not tanque:
            self.mostra_mensagem("Tanque não encontrado!", tipo='erro')
            return

        nome, tipo_combustivel, _, _, _, _, _ = tanque

        # Widgets para exibir informações
        info_label = ctk.CTkLabel(modal, text=f"Tanque: {nome}\nCombustível: {tipo_combustivel}")
        info_label.pack(pady=10)

        # Campo de entrada para a quantidade de abastecimento
        entrada_abastecimento = ctk.CTkEntry(modal)
        entrada_abastecimento.pack(pady=10)

        # Botão para confirmar o abastecimento
        confirm_button = ctk.CTkButton(modal, text="Confirmar",
                                       command=lambda: self.renovar_estoque(tanque_id, float(entrada_abastecimento.get())))
        confirm_button.pack(pady=10)

    def mostra_mensagem(self, mensagem, tipo='erro'):
        if tipo == 'erro':
            messagebox.showerror("Erro", mensagem)
        elif tipo == 'info':
            messagebox.showinfo("Informação", mensagem)
