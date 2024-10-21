import tkinter as tk
import tkinter.font as tkfont
import main
import achat
import livres
import auteurs
import clients
import emprunt
import editeurs

class Accueil:

    def __init__(self, window):
        """Ouvre la page d'accueil"""
        self.window = window
        font0 = tkfont.Font(family="Times New Roman", size=45)
        font1 = tkfont.Font(family="Times New Roman", size=20)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=2)
        self.window.grid_columnconfigure(0, weight=50)
        self.window.grid_columnconfigure(1, weight=1)

        self.lblaccueil = tk.Label(self.window, text="Accueil", font=font0)
        self.lblaccueil.grid(row=0)

        self.frame = tk.Frame(self.window)
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

        self.btn_retour = tk.Button(self.window, text="retour", font=font1, command=self.command_retour)
        self.btn_retour.grid(row = 2, column = 0)

    def command_achat(self):
        for widget in self.window.winfo_children(): #Suppresssion de tous les elements de la fenetre
            widget.destroy()
        achat.Achat(self.window)
        return

    def command_emprunt(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        emprunt.Emprunt(self.window)

    def command_clients(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        clients.Clients(self.window)

    def command_livres(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        livres.Livres(self.window)

    def command_auteurs(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        auteurs.Auteurs(self.window)

    def command_editeurs(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        editeurs.Editeurs(self.window)

    def command_retour(self):
        """Retourne au premier ecran"""
        for widget in self.window.winfo_children(): #Suppresssion de tous les elements de la fenetre
            widget.destroy()
        main.Main(self.window)              #On retourne a l'ecran precedent

if __name__ == '__main__':
    window = tk.Tk()
    window.geometry("1400x720")
    a = Accueil(window)
    tk.mainloop()
