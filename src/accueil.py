import tkinter as tk
import tkinter.font as tkfont
import main

window = None

class Accueil:

    def __init__(self):
        """Ouvre la page d'accueil"""
        global window
        font0 = tkfont.Font(family="Times New Roman", size=45)
        font1 = tkfont.Font(family="Times New Roman", size=20)

        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.grid_rowconfigure(2, weight=2)
        window.grid_columnconfigure(0, weight=50)
        window.grid_columnconfigure(1, weight=1)

        self.lblaccueil = tk.Label(window, text="Accueil", font=font0)
        self.lblaccueil.grid(row=0)

        self.frame = tk.Frame(window)
        self.frame.grid(row=1)

        self.btn_achat = tk.Button(self.frame, text="Achat", font=font1, command=self.command_achat)
        self.btn_achat.grid(row = 0, column = 0, padx = 72, pady = 103)
        self.btn_emprunt = tk.Button(self.frame, text="Emprunt", font=font1, command=self.command_emprunt)
        self.btn_emprunt.grid(row = 0, column = 1, padx = 72)
        self.btn_clients = tk.Button(self.frame, text="Clients", font=font1, command=self.command_clients)
        self.btn_clients.grid(row = 0, column = 2, padx = 72)
        self.btn_livres = tk.Button(self.frame, text="Livres", font=font1, command=self.command_livres)
        self.btn_livres.grid(row = 1, column = 0)
        self.btn_auteurs = tk.Button(self.frame, text="Auteurs", font=font1, command=self.command_auteurs)
        self.btn_auteurs.grid(row = 1, column = 1)
        self.btn_editeurs = tk.Button(self.frame, text="Editeurs", font=font1, command=self.command_editeurs)
        self.btn_editeurs.grid(row = 1, column = 2)

        self.btn_retour = tk.Button(window, text="retour", font=font1, command=self.command_retour)
        self.btn_retour.grid(row = 2, column = 0)

    def command_achat(self):
        return

    def command_emprunt(self):
        return

    def command_clients(self):
        return

    def command_livres(self):
        return

    def command_auteurs(self):
        return

    def command_editeurs(self):
        return

    def command_retour(self):
        # for widget in window.winfo_children():
        #     widget.destroy()
        #a = main()

if __name__ == '__main__':
    window = tk.Tk()
    window.geometry("1400x720")
    a = Accueil()
    tk.mainloop()
