import customtkinter as ctk
from controladores.controladorUsuario import ControladorUsuario
from tkinter import messagebox

class TelaLogin:
    def __init__(self):
        self.controlador_usuario = ControladorUsuario()
        self.login_sucesso = False
        self.is_gestor = False
        

    def modal_login(self):
        self.modal = ctk.CTk()
        self.modal.title("Login")
        self.modal.geometry("400x500")
        self.modal.resizable(False, False)
        self.modal._apply_appearance_mode("light")

        # Melhorar o fundo do modal
        self.modal.configure(bg="#D4D4D4")

        # Criar um frame para agrupar os widgets
        self.frame = ctk.CTkFrame(self.modal, corner_radius=15, width=350, height=350)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        # Adicionar widgets ao frame
        self.entry_usuario = ctk.CTkEntry(self.frame, placeholder_text="Usuário", width=300)
        self.entry_usuario.place(relx=0.5, rely=0.3, anchor='center')

        self.entry_senha = ctk.CTkEntry(self.frame, show="*", placeholder_text="Senha", width=300)
        self.entry_senha.place(relx=0.5, rely=0.5, anchor='center')

        self.button_login = ctk.CTkButton(self.frame, text="Login", command=self.login, width=150)
        self.button_login.place(relx=0.5, rely=0.7, anchor='center')

        self.modal.mainloop()

        return self.login_sucesso, self.is_gestor

    def login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if not usuario or not senha:
            self.mostra_mensagem("Usuário e senha são obrigatórios", 'erro')
            return

        try:
            if len(usuario) == 11 and usuario.isdigit():
                user = self.controlador_usuario.login_cpf(usuario, senha)
            else:
                user = self.controlador_usuario.login_email(usuario, senha)
            
            if user:
                self.login_sucesso = True
                self.is_gestor = user[1]  # Supondo que isgestor é a segunda coluna retornada
                self.mostra_mensagem("Login realizado com sucesso", 'info')
                self.modal.destroy()  # Fechar o modal após o sucesso do login
            else:
                self.mostra_mensagem("Usuário ou senha incorretos", 'erro')
        except Exception as e:
            self.mostra_mensagem(f"Erro ao realizar login: {str(e)}", 'erro')
        
        return self.login_sucesso, self.is_gestor

    def mostra_mensagem(self, mensagem, tipo='erro'):
        if tipo == 'erro':
            messagebox.showerror("Erro", mensagem)
        elif tipo == 'info':
            messagebox.showinfo("Informação", mensagem)
