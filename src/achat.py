import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk
from datetime import date
from query import *
window = None

class Achat:
    """Ecran de la table achat avec toutes les operation qui lui correspond"""
    def __init__(self):
        global window
        self.window=window
        #Recuperation des donnees de la table SQL
        self.conn = initConn()
        req = doQuery(self.conn, "SELECT * FROM ACHAT")
        
        #Label en haut de l'ecran nom de la table
        font0 = tkfont.Font(family="Arial", size=30, weight="bold")
        lbl1 = tk.Label(window, text="Achats", font=font0)
        lbl1.grid(column=1, row=0)

        



        #Configuration police d'ecriture tableau
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 17))
        style.configure("Treeview", font=('Calibri', 15))

        #Creation tableau
        self.table=ttk.Treeview(window, height=22)
        self.table.grid(column=0, row=1, columnspan=3)
        self.table['columns'] = ['NoAchat', 'ISBN', 'IDClient', 'DateAchat', 'QteAchat', 'PrixTotAchat']
        self.table.column('#0', width=0, stretch=0)
        self.table.column('NoAchat', width=120)
        self.table.column('ISBN', width=200)
        self.table.column('IDClient', width=120)
        self.table.column('DateAchat', width=140)
        self.table.column('QteAchat', width=140)
        self.table.column('PrixTotAchat', width=160)

        for e in self.table['columns']:
            self.table.heading(e, text=e)

        self.table.heading('NoAchat', text='Noachat')
        self.table.heading('ISBN', text='ISBN')
        self.table.heading('IDClient', text='IDClient')
        self.table.heading('DateAchat', text='DateAchat')
        self.table.heading('QteAchat', text='QteAchat')
        self.table.heading('PrixTotAchat', text='PrixTotAchat')

        #Remplissage tableau
        for i in range(len(req)):
            self.table.insert(parent = '', index = i, values=req[i])

        #Boutons nouvelle entree, supprimer et recherche
        font1 = tkfont.Font(family = "Arial", size=18)

        self.ButNew = tk.Button(window, text='Nouvel Achat', font=font1, command=self.commandBuy)
        self.ButNew.grid(row=2, column=0)
        
        self.ButDel = tk.Button(window, text='Supprimer Achat', font=font1, state='disabled', command=self.commandDel)
        self.ButDel.grid(row=2, column =1)

        self.ButSearch = tk.Button(window, text='Rechercher', font=font1, command=self.commandSearch)
        self.ButSearch.grid(row=2, column = 2)

        #Label Nouvelle entree
        self.lblnew = tk.Label(window, text="Nouvel Achat", font=font0)

        #Frame pour les entrees des nouveaux attributs qu'on cache au debut

        self.newframe=tk.Frame(window)
        self.newframevis=False   #Booleen pour la visibilite de la frame (et du label)


        #Attributs pour nouvelle entree
        font2 = tkfont.Font(family="Calibri", size = 30)
        self.lblISBN = tk.Label(self.newframe, text="ISBN", font=font2)
        self.lblISBN.grid(row=0, sticky='nsew')
        self.entISBN = tk.Entry(self.newframe)
        self.entISBN.grid(row=1)

        self.lblIDClient = tk.Label(self.newframe, text="IDClient", font=font2)
        self.lblIDClient.grid(row=2, column=0)
        self.entIDClient = tk.Entry(self.newframe)
        self.entIDClient.grid(row=3)

        self.lblQteAchat = tk.Label(self.newframe, text="QteAchat", font=font2)
        self.lblQteAchat.grid(row=4)
        self.entQteAchat = tk.Entry(self.newframe)
        self.entQteAchat.grid(row=5)

        self.btnconfAchat = tk.Button(self.newframe, text='Confirmer', font=font1, command=self.commandConfBuy)
        self.btnconfAchat.grid(row=6)

        #Creation du label indiquant par la suite si l'operation a reussie ou non
        self.lblopstate = tk.Label(self.newframe, text="")
        self.lblopstate.grid(row=7)

    def updatetable(self):
        """Met à jour l'affichage du tableau"""
        #Suppression des elements
        for line in self.table.get_children():
            self.table.delete(line)

        #Remplissage avec les nouveaux elements
        req = doQuery(self.conn, "SELECT * FROM ACHAT")
        for i in range(len(req)):
            self.table.insert(parent = '', index = i, values=req[i])

        

    def commandBuy(self):
        """Affiche l'interface pour ajouter une nouvelle entree a la table"""
        self.ButNew.configure(state="disabled")
        self.newframe.grid(column=3, row = 1, sticky="nsew")
        self.lblnew.grid(column=3, row=0)
        self.newframevis = True
        #TODO: Trouver le moyen de les decaler un peu sur la droite, peut etre avec rowconfigure
    
    def commandSearch(self):
        """Affiche l'interface pour effectuer une recherche"""
        #TODO
        return

    def commandDel(self):
        """Supprime l'entree selectionnee"""
        #TODO
        return

    def commandConfBuy(self):
        """Confirme un achat (envoie la requete SQL a la BDD pour ajouter une entree a la table Achat)"""
        #Recuperation des valeurs de la nouvelle entree
        isbn = self.entISBN.get()
        idclient = self.entIDClient.get()
        qteachat = self.entQteAchat.get()
        dateachat = date.today().strftime("%d/%m/%Y")
        
        try:
            doNoReturnQuery(self.conn, f"INSERT INTO Achat (ISBN, IDClient, DateAchat, QteAchat) VALUES('{isbn}', {idclient}, '{dateachat}', {qteachat});")
            self.lblopstate.config(text = "Opération Réussie", fg="green")
            self.updatetable()
        except:
            self.lblopstate.config(text = "Opétation échouée, revoyez les entrées", fg="red")
            doNoReturnQuery(self.conn, "ROLLBACK;")
        
        


if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("1400x720")
    a = Achat()
    tk.mainloop()