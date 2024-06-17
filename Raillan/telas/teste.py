import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        frame_tanque = ctk.CTkFrame(self, relief="solid", borderwidth=1, padding=10, corner_radius=10, shadow=True, shadow_color="black")
        frame_tanque.pack(fill="x", padx=20, pady=10)
        progressbar = customtkinter.CTkProgressBar(frame_tanque, orientation="vertical", progress_color="green")
        progressbar.grid(row=1, column=0, padx=20, pady=20)
        progressbar.set(0.5)
        botao = customtkinter.CTkButton(frame_tanque, text="Botão",hover=True,hover_color="blue")
        botao.grid(row=2, column=0, padx=20, pady=20)





app = App()
app.mainloop()
