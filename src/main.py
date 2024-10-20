import tkinter as tk
import tkinter.font as tkfont
import accueil


class Main:
    def __init__(self, window):
        """Classe qu'on lance pour ouvrir l'application, notamment les 2 premiers écrans"""
        self.window = window
        font0 = tkfont.Font(family = "Times New Roman", size = 60)
        font1 = tkfont.Font(family = "Times New Roman", size = 20)

        self.window.grid_rowconfigure(0, weight=3)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)


        self.lbltitre = tk.Label(self.window, text="Libre et Ris", font=font0)
        self.lbltitre.grid(row = 0, column=1, sticky="nsew")
        self.bouton = tk.Button(self.window, text="Ouvrir la caisse", font=font1, command=self.command_open)
        self.bouton.grid(row=1, column = 1)

    def command_open(self):
        """Affiche l'ecran d'accueil"""
        for widget in self.window.winfo_children(): #Suppresssion de tous les elements de la fenetre
            widget.destroy()
        accueil.Accueil(self.window)


if __name__ == '__main__':
    window = tk.Tk()
    window.geometry("1400x720")
    a = Main(window)
    tk.mainloop()