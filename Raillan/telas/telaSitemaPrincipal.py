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

class MenuPrincipal(ctk.CTk):
    def __init__(self, is_gestor):
        super().__init__()
        self.is_gestor = is_gestor

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
        self.create_frames()

        # Atualizar as cores do texto de acordo com o tema
        self.update_text_colors()

        # Bind para mudança de tema
        ctk.set_appearance_mode("light")
        self.update_text_colors()


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

        icon_path_base = "/Users/railanabreu/Documents/Projects/GasGuardian/Raillan/telas/Icones/"

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


        for frame in self.frames.values():
            frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
            frame.grid_remove()  # Ocultar todos os frames inicialmente

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
        self.show_frame(selected_item)

    def show_frame(self, frame_name):
        # Ocultar todos os frames
        if self.current_frame:
            self.current_frame.grid_remove()

        # Mostrar o frame selecionado
        frame = self.frames.get(frame_name)
        if frame:
            frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
            self.current_frame = frame

    def update_text_colors(self):
        theme = ctk.get_appearance_mode()
        if theme == "Dark":
            text_color = "white"
        else:
            text_color = "black"

        # Atualizar as cores das tags
        self.tree_menu.tag_configure("main", foreground=text_color)
        self.tree_menu.tag_configure("sub", foreground=text_color)

        # Atualizar a cor do label do menu
        self.menu_label.configure(text_color=text_color)

        # Atualizar a cor do texto no Treeview
        self.tree_menu.tag_configure("main", foreground=text_color)
        self.tree_menu.tag_configure("sub", foreground=text_color)

    def on_theme_change(self, event=None):
        self.update_text_colors()

if __name__ == '__main__':
    ctk.set_appearance_mode("light")  # Usar o modo do sistema
    app = MenuPrincipal(is_gestor=True)  # Alterar conforme necessário para testes
    app.mainloop()
