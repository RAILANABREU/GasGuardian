import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from .TelaTanqueCombustivel import TelaTanqueCombustivel  # Importação da classe TelaTanqueCombustivel
from .telaBombaCombustivel import TelaBombaCombustivel  # Importação da classe TelaBombaCombustivel
from .TelaPosto import TelaPosto  # Importação da classe TelaPosto
from .telaAbastecimento import TelaAbastecimento  # Importação da classe TelaAbastecimento
from .telaUsuarios import TelaUsuario  # Importação da classe TelaUsuario
from .telaTipoCombustivel import TelaTipoCombustivel  # Importação da classe TelaTipoCombustivel
from .TelaRelatorios import TelaRelatorios  # Importação da classe TelaRelatorios
from .TelaRenovacaoEstoque import TelaRenovacaoEstoque  # Importação da classe TelaRenovacaoEstoque

class MenuPrincipal(ctk.CTk):
    def __init__(self, is_gestor, controlador_sistema):
        super().__init__()
        self.is_gestor = is_gestor
        self.controlador_sistema = controlador_sistema

        self.title("Sistema de Gerenciamento")
        self.geometry("1200x800")

        # Inicializar a lista de imagens
        self.images = []

        # Configurando a estrutura do menu lateral e o container principal
        self.configure_grid()
        self.create_menu()

        # Inicializando os frames
        self.frames = {}
        self.current_frame = None

        # Criar os frames após a configuração do menu
        self.create_frames()

        # Atualizar as cores do texto de acordo com o tema
        ctk.set_appearance_mode("light")

    def configure_grid(self):
        self.grid_columnconfigure(0, weight=0, minsize=300)  # Largura fixa do menu
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

    def create_menu(self):
        # Menu lateral
        self.menu_frame = ctk.CTkFrame(self, width=200)
        self.menu_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        # Label do Menu
        self.menu_label = ctk.CTkLabel(self.menu_frame, text="Posto do Chico", font=("Arial", 30, "bold"))
        self.menu_label.pack(pady=20)

        self.tree_menu = ttk.Treeview(self.menu_frame, show="tree", selectmode="browse")
        self.tree_menu.pack(fill="both", expand=True)

        # Ajustar a altura das linhas
        style = ttk.Style()
        style.configure("Treeview", rowheight=50)

        icon_path_base = "Raillan/telas/Icones/"

        if self.is_gestor == 1:
            # Adicionando itens ao menu
            self.add_menu_item("", "abastecimento", "Abastecimento", icon_path_base + "fuel-pump.png", True)
            cadastro_id = self.add_menu_item("", "cadastro", "Cadastro", icon_path_base + "cadastro.png", True)
            self.add_menu_item(cadastro_id, "funcionarios", "Funcionários", icon_path_base + "Funcionarios.png")
            self.add_menu_item(cadastro_id, "tanques", "Tanques", icon_path_base + "tanquesCombustivel.png")
            self.add_menu_item(cadastro_id, "combustiveis", "Combustíveis", icon_path_base + "oil.png")
            self.add_menu_item(cadastro_id, "bombas", "Bombas", icon_path_base + "bomba-de-gasolina.png")
            self.add_menu_item(cadastro_id, "posto", "Posto", icon_path_base + "posto.png")
            self.add_menu_item("", "relatorios", "Relatórios", icon_path_base + "relatorios.png", True)
            estoque_id = self.add_menu_item("", "Estoque", "Estoque", icon_path_base + "oil-tank.png", True)
            self.add_menu_item(estoque_id, "Renovacao", "Renovacão", icon_path_base + "oil-tanker.png")
        else:
            self.add_menu_item("", "abastecimento", "Abastecimento", icon_path_base + "fuel-pump.png", True)

        # Botão de logout
        self.logout_button = ctk.CTkButton(self.menu_frame, text="Logout", command=self.logout)
        self.logout_button.pack(side="bottom", pady=20)

        # Configuração das tags
        self.tree_menu.tag_configure("main", font=("Arial", 30, "bold"))
        self.tree_menu.tag_configure("sub", font=("Arial", 25, "bold"))

        self.tree_menu.bind("<<TreeviewSelect>>", self.on_menu_select)

    def create_frames(self):
        # Adicionar os frames que você deseja exibir ao clicar nos submenus
        self.frames["tanques"] = TelaTanqueCombustivel(self)
        self.frames["bombas"] = TelaBombaCombustivel(self)
        self.frames["posto"] = TelaPosto(self)
        self.frames["abastecimento"] = TelaAbastecimento(self)
        self.frames["funcionarios"] = TelaUsuario(self)
        self.frames["combustiveis"] = TelaTipoCombustivel(self)
        self.frames["relatorios"] = TelaRelatorios(self)
        self.frames["Renovacao"] = TelaRenovacaoEstoque(self)

    def add_menu_item(self, parent, id, text, icon_path, is_main=False):
        icon = self.get_icon(icon_path)
        if icon:
            return self.tree_menu.insert(parent, "end", id, text=" " + text, image=icon, tags=("main" if is_main else "sub",))
        else:
            return self.tree_menu.insert(parent, "end", id, text=text, tags=("main" if is_main else "sub",))

    def get_icon(self, path):
        if os.path.exists(path):
            image = Image.open(path)
            image = image.resize((25, 25), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.images.append(photo)  # Adiciona a imagem à lista para evitar coleta de lixo
            return photo
        else:
            return None

    def on_menu_select(self, event):
        selected_item = self.tree_menu.selection()[0]
        if selected_item in self.frames:
            self.show_frame(selected_item)

    def show_frame(self, frame_name):
        # Ocultar todos os frames
        for frame in self.frames.values():
            frame.grid_remove()

        # Remover o frame antigo do grid e destruir
        if self.current_frame:
            self.current_frame.grid_remove()
            self.current_frame.destroy()
            self.current_frame = None

        # Criar e mostrar o frame selecionado
        frame = self.frames.get(frame_name)
        if frame:
            new_frame = frame.__class__(self)  # Criar uma nova instância do frame
            new_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
            self.current_frame = new_frame
            if hasattr(new_frame, 'criar_tela'):
                new_frame.criar_tela()  # Chamar o método criar_tela se ele existir

    def logout(self):
        self.destroy()
        self.controlador_sistema.iniciar()  # Reinicia o sistema e mostra a tela de login

if __name__ == '__main__':
    ctk.set_appearance_mode("light")  # Usar o modo do sistema
    controlador_sistema = None  # Alterar conforme necessário para testes
    app = MenuPrincipal(is_gestor=True, controlador_sistema=controlador_sistema)  # Alterar conforme necessário para testes
    app.mainloop()
