import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk
from query import *
window = None

class Achat:
    """Ecran de la table achat avec toutes les operation qui lui correspond"""
    def __init__(self):
        #Recuperation des donnees de la table SQL
        self.conn = initConn()
        req = doQuery(self.conn, "SELECT * FROM ACHAT")
        
        #Label en haut de l'ecran 
        font0 = tkfont.Font(family="Arial", size=30, weight="bold")
        lbl1 = tk.Label(window, text="Achats", font=font0)
        lbl1.pack(side="top")

        #Configuration police d'ecriture tableau
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 17))
        style.configure("Treeview", font=('Calibri', 15))

        #Creation tableau
        self.table=ttk.Treeview(window, height=22)
        self.table.pack(side="top", padx=50, pady=40, anchor=tk.W)
        self.table['columns'] = ['NoAchat', 'ISBN', 'IDClient', 'DateAchat', 'QteAchat', 'PrixTotAchat']
        self.table.column('#0', width=0, stretch=0)
        self.table.column('NoAchat', width=120)
        self.table.column('ISBN', width=200)
        self.table.column('IDClient', width=120)
        self.table.column('DateAchat', width=140)
        self.table.column('QteAchat', width=140)
        self.table.column('PrixTotAchat', width=160)

        self.table.heading('NoAchat', text='Noachat')
        self.table.heading('ISBN', text='ISBN')
        self.table.heading('IDClient', text='IDClient')
        self.table.heading('DateAchat', text='DateAchat')
        self.table.heading('QteAchat', text='QteAchat')
        self.table.heading('PrixTotAchat', text='PrixTotAchat')
        #self.table['show'] = 'headings'

        #Remplissage tableau
        for i in range(len(req)):
            self.table.insert(parent = '', index = i, values=req[i])

        #Boutons nouvelle entree, supprimer et recherche
        font1 = tkfont.Font(family = "Arial", size=18)

        self.ButNew = tk.Button(window, text='Nouvel Achat', font=font1, command=self.commandBuy)
        self.ButNew.pack(side='left', padx=70)
        
        self.ButDel = tk.Button(window, text='Supprimer Achat', font=font1, state='disabled', command=self.commandDel)
        self.ButDel.pack(side='left', padx=70)

        self.ButSearch = tk.Button(window, text='Rechercher', font=font1, command=self.commandSearch)
        self.ButSearch.pack(side='left', padx=70)

    def commandBuy(self):
        """Affiche l'interface pour ajouter une nouvelle entree a la table"""
        #TODO
        return
    
    def commandSearch(self):
        """Affiche l'interface pour effectuer une recherche"""
        #TODO
        return

    def commandDel(self):
        """Supprime l'entree selectionnee"""
        #TODO
        return



if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("1400x720")
    a = Achat()
    tk.mainloop()