import tkinter as tk
import tkinter.font as tkfont

window = None

class Main:
    def __init__(self):
        """Classe qu'on lance pour ouvrir l'application, notamment les 2 premiers écrans"""
        global window
        font0 = tkfont.Font(family = "Times New Roman", size = 60)
        font1 = tkfont.Font(family = "Times New Roman", size = 20)

        window.grid_rowconfigure(0, weight=3)
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        window.grid_columnconfigure(2, weight=1)


        self.lbltitre = tk.Label(window, text="Libre et Ris", font=font0)
        self.lbltitre.grid(row = 0, column=1, sticky="nsew")
        self.bouton = tk.Button(window, text="Ouvrir la caisse", font=font1, command=self.command_open)
        self.bouton.grid(row=1, column = 1)

    def command_open(self):
        return


if __name__ == '__main__':
    window = tk.Tk()
    window.geometry("1400x720")
    a = Main()
    tk.mainloop()